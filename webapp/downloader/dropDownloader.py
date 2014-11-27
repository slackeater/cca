from models import FileMetadata,AccessToken, Download, FileDownload, FileHistory
import json, base64, os, md5, dropbox, requests
from django.conf import settings
from webapp.func import dropboxAlternateName



def getMetaData(at):
	""" Get the metadata """
	m = json.loads(base64.b64decode(FileMetadata.objects.get(tokenID=at).metadata))
	return m

def downloadMetaData(client,at):
	""" Download metadata """

	#root
	root = client.metadata("/",include_deleted=True,include_media_info=True)

	fileMetaData = json.dumps(recurseDropTree(root,client,5))

	fm = FileMetadata.objects.filter(tokenID=at)

	if fm.count() == 0:
		storeFM = FileMetadata(metadata=base64.b64encode(fileMetaData),tokenID=at)
		storeFM.save()

		return "running","-",1

def recurseDropTree(folderMetadata, client, depth):
	""" Recurse in each folder """
	res = list()
	
	if folderMetadata['is_dir'] and depth > 0:

		res.append(folderMetadata)

		#get content
		for c in folderMetadata['contents']:
			if c['is_dir']:
				metadata = client.metadata(c['path'])
				# go down one level in the tree
				myres = recurseDropTree(metadata, client, depth-1)
				res += myres
				
		return res

	elif folderMetadata['is_dir'] and depth == 0:
		res.append(folderMetadata)
		return res

def downloadFiles(client,at):
	""" Download files """

	meta = getMetaData(at)
	downDir = Download.objects.get(tokenID=at).folder
	downDirFull = os.path.join(settings.DOWNLOAD_DIR,downDir)
	downDirFullSub = os.path.join(downDirFull, "files")

	if not os.path.isdir(downDirFull):
		os.mkdir(downDirFull)

	if not os.path.isdir(downDirFullSub):
		os.mkdir(downDirFullSub)
	
	#for each folder
	for c in meta:
		#for each file in folder
		for f in c['contents']:
			if not f['is_dir']: # if is a file
				#compute the alternateName
				altName = dropboxAlternateName(f['path'],f['modified'])

				bName = os.path.basename(f['path'])
				
				try:
					with client.get_file(f['path']) as f:
						outF = open(os.path.join(downDirFullSub,bName+"_"+altName),"wb+")
						outF.write(f.read())
						outF.close()
						fDb = FileDownload(fileName=bName,alternateName=altName,status=1,tokenID=at)
						fDb.save()
				except dropbox.rest.ErrorResponse as e:
					
					if e.status == 404:
						#file has been deleted , status=2
						f = FileDownload(fileName=bName,alternateName=altName,status=2,tokenID=at)
						f.save()
					else:
						raise e

				
	
	return "running","-",2
	
def downloadHistory(client,at):
	""" Download the history for dropbox """

	meta = getMetaData(at)
	downDir = Download.objects.get(tokenID=at).folder
	downDirFull = os.path.join(settings.DOWNLOAD_DIR,downDir)
	downDirFullSub = os.path.join(downDirFull,"history")

	if not os.path.isdir(downDirFull):
		os.mkdir(downDirFull)

	if not os.path.isdir(downDirFullSub):
		os.mkdir(downDirFullSub)

	for c in meta:
		#for each file in folder
		for f in c['contents']:
			if not f['is_dir']:
				rev = client.revisions(f['path'])
				
				if len(rev) >= 1: # one revision means original file
					#compute alternate name for db lookup
					modified = rev[0]['modified']
					path = rev[0]['path']
					s = path.encode('utf-8') + modified.encode('utf-8')
					altName = md5.new(s).hexdigest()

					bName = os.path.basename(path)
					#get file download id
					fDown = FileDownload.objects.get(fileName=bName,alternateName=altName,tokenID=at)
					print s
					print altName
					print fDown.id
					del rev[0]
					
					# create a directory to store file revision
					revPath = os.path.join(downDirFullSub,altName)
					if not os.path.isdir(revPath):
						os.mkdir(revPath)

					for r in rev:
						rEnc = base64.b64encode(json.dumps(r))
						revID = r['rev']
						print "-" + str(revID)
						
						#get revision
						with client.get_file(f['path'],revID) as revF:
							outF = open(os.path.join(revPath,bName+"_"+revID),"wb+")
							outF.write(revF.read())
							outF.close()
							fDb = FileHistory(revision=revID,status=1,fileDownloadID=fDown,revisionMetadata=rEnc)
							fDb.save()

	return "running","-",3

def sharedFolder(client,at):
	""" Find the shared folders """

	#get list of shared folders
	#response = requests.get('https://api.dropbox.com/1/shared_folders/',headers={'Authorization':'Bearer %s' % base64.b64decode(at.accessToken))

	#TODO
