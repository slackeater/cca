from models import FileMetadata,AccessToken, Download, FileDownload, FileHistory
import json, base64, os, md5, dropbox, requests,sys,time
from django.conf import settings
from webapp.func import dropboxAlternateName
from django.utils import timezone
from django.utils.dateformat import format
from webapp import constConfig
from abstractDownloader import AbstractDownloader

# add path for crypto
cryptoPath = os.path.join(os.path.dirname(settings.BASE_DIR), "finder")

if not cryptoPath in sys.path:
	sys.path.insert(1, cryptoPath)
	del cryptoPath

import crypto

class DropboxDownloader(AbstractDownloader):

	def __init__(self,download,uname,pwd):
		AbstractDownloader.__init__(self,download,uname,pwd)

	def createService(self):
		c = dropbox.client.DropboxClient(base64.b64decode(self.t.accessToken))
		self.service = c

	def downloadMetaData(self,simulateDownload = False):
		""" Download metadata """

		#used for test
		if simulateDownload is True:
			time.sleep(constConfig.TEST_THREAD_SLEEP_TIME)
			return downStatus

		#root
		root = self.service.metadata("/",include_deleted=True,include_media_info=True)

		fileMetaData = self.recurseDropTree(root,5)
		
		self.metadata = fileMetaData
		meta = base64.b64encode(json.dumps(fileMetaData))
		metaTime = timezone.now()
		metaHash = crypto.rsaSignatureSHA256(meta+crypto.HASH_SEPARATOR+format(metaTime,"U"),settings.PRIV_KEY)

		storeFM = FileMetadata(metadata=meta,tokenID=self.t,metaTime=metaTime,metadataHash=metaHash)
		storeFM.save()

		self.d.threadStatus = constConfig.THREAD_DOWN_META
		self.d.save()

	def recurseDropTree(self,folderMetadata,depth):
		""" Recurse in each folder """
		res = list()
		
		if folderMetadata['is_dir'] and depth > 0:

			res.append(folderMetadata)

			#get content
			for c in folderMetadata['contents']:
				if c['is_dir']:
					metadata = self.service.metadata(c['path'])
					# go down one level in the tree
					myres = self.recurseDropTree(metadata,depth-1)
					res += myres
					
			return res

		elif folderMetadata['is_dir'] and depth == 0:
			res.append(folderMetadata)
			return res

	def computeDownload(self):
	
		totalSize = long(0)

		for f in self.metadata:
			for c in f['contents']:
				totalSize += long(c['bytes'])

		self.d.downloadSize = totalSize
		self.d.threadStatus = constConfig.THREAD_COMPUTING
		self.d.save()

	def downloadFiles(self,simulateDownload = False):
		""" Download files """

		#used for test
		if simulateDownload is True:
			time.sleep(constConfig.TEST_THREAD_SLEEP_TIME)
			return downStatus

		downDirFullSub = os.path.join(self.downloadDir, "files")

		if not os.path.isdir(downDirFullSub):
			os.mkdir(downDirFullSub)
		
		#for each folder
		for c in self.metadata:
			#for each file in folder
			for f in c['contents']:
				if not f['is_dir']: # if is a file
					#compute the alternateName
					altName = dropboxAlternateName(f['path'],f['modified'])

					bName = os.path.basename(f['path'])
					
					try:
						with self.service.get_file(f['path']) as f:
							hashName = crypto.sha256(bName+crypto.HASH_SEPARATOR+altName).hexdigest()
							fullPath = os.path.join(downDirFullSub,hashName+"_"+altName)
							outF = open(fullPath,"wb+")
							outF.write(f.read())
							outF.close()
							h = crypto.rsaSignatureSHA256(fullPath,settings.PRIV_KEY,True)
							fDb = FileDownload(fileName=bName,alternateName=altName,status=1,tokenID=self.t,fileHash=h)
							fDb.save()
					except dropbox.rest.ErrorResponse as e:
						
						if e.status == 404:
							#file has been deleted , status=2
							f = FileDownload(fileName=bName,alternateName=altName,status=2,tokenID=self.t)
							f.save()
						else:
							raise e

	def downloadHistory(self,simulateDownload = False):
		""" Download the history for dropbox """

		#used for test
		if simulateDownload is True:
			time.sleep(constConfig.TEST_THREAD_SLEEP_TIME)
			return downStatus

		downDirFullSub = os.path.join(self.downloadDir,"history")

		if not os.path.isdir(downDirFullSub):
			os.mkdir(downDirFullSub)

		for c in self.metadata:
			#for each file in folder
			for f in c['contents']:
				if not f['is_dir']:
					rev = self.service.revisions(f['path'])
					
					if len(rev) > 1: # one revision means original file
						#compute alternate name for db lookup, from the first revision that is the original file
						modified = rev[0]['modified']
						path = rev[0]['path']
						s = path.encode('utf-8') + modified.encode('utf-8')
						altName = md5.new(s).hexdigest()

						bName = os.path.basename(path)
						#get file download id
						fDown = FileDownload.objects.get(fileName=bName,alternateName=altName,tokenID=self.t)
						del rev[0]
						
						# create a directory to store file revision
						revPath = os.path.join(downDirFullSub,altName)
						if not os.path.isdir(revPath):
							os.mkdir(revPath)

						for r in rev:
							revID = r['rev']
							
							#get revision
							with self.service.get_file(f['path'],revID) as revF:
								hashName = crypto.sha256(bName+crypto.HASH_SEPARATOR+revID).hexdigest()
								fullPath = os.path.join(revPath,hashName+"_"+revID)
								outF = open(fullPath,"wb+")
								outF.write(revF.read())
								outF.close()

								#hash
								rEnc = base64.b64encode(json.dumps(r))
								downloadTime = timezone.now()
								fileRevisionHash = crypto.rsaSignatureSHA256(fullPath,settings.PRIV_KEY,True)
								revisionMetadataHash = crypto.rsaSignatureSHA256(rEnc+crypto.HASH_SEPARATOR+format(downloadTime,"U"),settings.PRIV_KEY)

								fDb = FileHistory(
										revision=revID,
										status=1,
										fileDownloadID=fDown,
										revisionMetadata=rEnc,
										downloadTime=downloadTime,
										revisionMetadataHash=revisionMetadataHash,
										fileRevisionHash=fileRevisionHash
									)
								fDb.save()


	def downloadFileHistory(self):
		self.downloadFiles()
		self.downloadHistory()
		self.d.threadStatus = constConfig.THREAD_DOWN_FH
		self.d.save()

	def sharedFolder(client,at):
		""" Find the shared folders """

		#get list of shared folders
		#response = requests.get('https://api.dropbox.com/1/shared_folders/',headers={'Authorization':'Bearer %s' % base64.b64decode(at.accessToken))

		#TODO
