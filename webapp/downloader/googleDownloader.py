from models import AccessToken,FileDownload,FileMetadata,FileHistory,Download
import base64,json,os,sys,time
from apiclient import errors
from django.conf import settings
from django.utils import timezone
from webapp.func import getTimestamp
from webapp import constConfig
import httplib2
from oauth2client.client import OAuth2Credentials
from apiclient.discovery import build
from abstractDownloader import AbstractDownloader
from django.core.exceptions import ObjectDoesNotExist

# add path for crypto
cryptoPath = os.path.join(os.path.dirname(settings.BASE_DIR), "finder")

if not cryptoPath in sys.path:
	sys.path.insert(1, cryptoPath)
	del cryptoPath

import crypto

class GoogleDownloader(AbstractDownloader):

	def __init__(self,download,uname,pwd):
		AbstractDownloader.__init__(self,download,uname,pwd)

	def createService(self):
		http = httplib2.Http()
		credentials = OAuth2Credentials.from_json(base64.b64decode(self.t.accessToken))
		credAuth = credentials.authorize(http)
		self.service = build("drive","v2",http=credAuth)

	def downloadMetaData(self,simulateDownload = False):
		""" Download the metadata """

		#used for tests
		if simulateDownload is True:
			#simulate the download by waiting 10 seconds
			time.sleep(constConfig.TEST_THREAD_SLEEP_TIME)
			return downStatus
		
		#download
		result = []
		page_token = None

		while True:
			param = {}

			if page_token:
				param['pageToken'] = page_token
				param['maxResults'] = 500
			
			files = self.service.files().list(**param).execute()
			result.extend(files['items'])
			page_token = files.get('nextPageToken')
			
			if not page_token:
				break


		self.metadata = result
		
		meta = base64.b64encode(json.dumps(self.metadata))

		metaTime = timezone.now()
		
		txt = meta+crypto.HASH_SEPARATOR+format(metaTime,"U")
		metaHash = crypto.rsaSignatureSHA256(txt,settings.PRIV_KEY)

		storeFM = FileMetadata(metadata=meta,tokenID=self.t,metaTime=metaTime,metadataHash=metaHash)
		storeFM.save()

		self.d.threadStatus = constConfig.THREAD_DOWN_META
		self.d.save()

	def computeDownload(self):
	
		totalSize = long(0)
			
		for item in self.metadata:

			if "quotaBytesUsed" in item:
				totalSize += long(item['quotaBytesUsed'])
			elif "fileSize" in item:
				totalSize += long(item['fileSize'])

		self.d.downloadSize = totalSize
		self.d.threadStatus = constConfig.THREAD_COMPUTING
		self.d.save()

	def downloadFiles(self,simulateDownload = False):
		""" Download file with google drive """

		#used for tests
		if simulateDownload is True:
			#simulate the download by waiting 10 seconds
			time.sleep(constConfig.TEST_THREAD_SLEEP_TIME)
			return downStatus
		
		#get download folder
		downDirFullSub = os.path.join(self.downloadDir,"files")
		
		if not os.path.isdir(downDirFullSub):
			os.mkdir(downDirFullSub)
	
		myFile = open("/home/snake/downFIles.txt","w")

		#iterate over file and write to disk
		for item in self.metadata:
				if 'downloadUrl' in item:
					url = item['downloadUrl']
				elif 'exportLinks' in item:
					url = item['exportLinks']["application/pdf"]
				else:
					url = None

				if url != None:
					
					fileDb = None

					try:
						resp, content = self.service._http.request(url)
						
						if resp.status == 200:
							hashFileName = crypto.sha256(item['title']+crypto.HASH_SEPARATOR+item['id'])
							fullName = os.path.join(downDirFullSub,hashFileName.hexdigest()+ "_" + item['id'])
							
							with open(fullName,"wb+") as f:
								f.write(content)
							
							#compute hash
							h = crypto.rsaSignatureSHA256(fullName,settings.PRIV_KEY,True)
						else:
							h = "-"

						fileDb = FileDownload(fileName=item['title'],alternateName=item['id'],status=resp.status,tokenID=self.t,fileHash=h)
						fileDb.save()
						myFile.write(str(vars(fileDb)))
					except errors.HttpError, e:
						#store this entry with the exception code
						fileDb = FileDownload(fileName=item['item'],alternateName=item['id'],status=e.resp.status,tokenID=self.t,fileHash="-")
						fileDb.save()

	def downloadHistory(self,simulateDownload = False):
		""" Download the history for a file """

		#used for tests
		if simulateDownload is True:
			#simulate the download by waiting 10 seconds
			time.sleep(constConfig.TEST_THREAD_SLEEP_TIME)
			return downStatus

		downDirHistory = os.path.join(self.downloadDir,"history")

		if not os.path.isdir(downDirHistory):
			os.mkdir(downDirHistory)

		for item in self.metadata:
			#folders do not support revision
			if item['mimeType'] != 'application/vnd.google-apps.folder':

				fh = None
				try:
					fileDownload = FileDownload.objects.get(fileName=item['title'],alternateName=item['id'],tokenID=self.t,status=200)

					try:
						#get revisions for this file
						revs = self.service.revisions().list(fileId=item['id']).execute()
					
						if len(revs['items']) > 1:

							#create a folder for this file
							revPath = os.path.join(downDirHistory,item['id'])
							if not os.path.isdir(revPath):
								os.mkdir(revPath)

							#get file download
							print item['title']
							print item['id']
								
							for r in revs['items']:

								if 'exportLinks' in r:
									url = r['exportLinks']["application/pdf"]
								elif 'downloadUrl' in r:
									url = r['downloadUrl']
								else:
									url = None

								if url != None:
									resp, content = self.service._http.request(url)
								
									revItem = base64.b64encode(json.dumps(r))
									revID = r['id']
									hashFileName = crypto.sha256(item['title']+crypto.HASH_SEPARATOR+revID)
									downloadTime = timezone.now()
									revisionMetadataHash = crypto.rsaSignatureSHA256(
											revItem+crypto.HASH_SEPARATOR+getTimestamp(downloadTime),
											settings.PRIV_KEY)

									#if the response is affirmative store the file
									if resp.status == 200:

										fullName = os.path.join(revPath,hashFileName.hexdigest()+"_"+revID)

										with open(fullName,"wb+") as f:
											f.write(content)

										# compute hash
										fileRevisionHash = crypto.rsaSignatureSHA256(fullName,settings.PRIV_KEY,True)
									else:
										fileRevisionHash = "-"

									fh = FileHistory(
										revision=revID,
										status=resp.status,
										fileDownloadID=fileDownload,
										revisionMetadata=revItem,
										downloadTime=downloadTime,
										fileRevisionHash=fileRevisionHash,
										revisionMetadataHash=revisionMetadataHash
										)
				
									fh.save()
					# HTTP when requesting history list or downloading file
					except errors.HttpError, e:
						fh = FileHistory(revision="-",status=e.resp.status,fileDownloadID=fileDownload,revisionMetadata="-",fileRevisionHash="-",revisionMetadataHash="-")
						fh.save()
				#we cannot download the history for a file that has not been downloaded correctly
				except ObjectDoesNotExist as e:
					print e
					pass

	def downloadFileHistory(self):
		self.downloadFiles()
		self.downloadHistory()
		self.d.threadStatus = constConfig.THREAD_DOWN_FH
		self.d.save()
