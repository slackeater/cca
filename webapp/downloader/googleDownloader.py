from models import AccessToken,FileDownload,FileMetadata,FileHistory,Download
import base64,json,os
from apiclient import errors
from django.conf import settings

def getMetaData(at):
	""" Get the metadata """
	m = json.loads(base64.b64decode(FileMetadata.objects.get(tokenID=at).metadata))
	return m

def uploadStatus(at,status,threadStatus,threadMessage):
	downloadItem = Download.objects.get(tokenID=at)
	
	#metadata downloaded and stored
	downloadItem.status = status
	downloadItem.threadStatus = threadStatus
	downloadItem.threadMessage = threadMessage
	downloadItem.save()

def downloadMetaData(driveService,at):
	""" Download the metadata """

	#download
	fileMetaData = json.dumps(driveService.files().list().execute())
	
	#store
	fm = FileMetadata.objects.filter(tokenID=at)

	# we do not have any record for this token
	if fm.count() == 0:
		storeFM = FileMetadata(metadata=base64.b64encode(fileMetaData),tokenID=at)
		storeFM.save()

		uploadStatus(at,1,"running","-")

		return True

def downloadFiles(driveService,at):
	""" Download file with google drive """

	meta = getMetaData(at)	
	downDir = Download.objects.get(tokenID=at).folder
	downDirFull = os.path.join(settings.DOWNLOAD_DIR,downDir)
	downDirFullSub = os.path.join(settings.DOWNLOAD_DIR,downDir,"files")
	

	#create directory if necessary
	if not os.path.isdir(downDirFull):
		os.mkdir(downDirFull)

	if not os.path.isdir(downDirFullSub):
		os.mkdir(downDirFullSub)

	#iterate over file and write to disk
	for item in meta['items']:
		if 'downloadUrl' in item:
			url = item['downloadUrl']
		elif 'exportLinks' in item:
			url = item['exportLinks']['application/pdf']

		resp, content = driveService._http.request(url)
		
		if resp.status == 200:
			fullName = os.path.join(downDirFullSub,item['title'] + "_" + item['id'])

			f = open(fullName,"wb+")
			f.write(content)
			f.close()

			fileDb = FileDownload(fileName=item['title'],alternateName=item['id'],status=1,tokenID=at)
			fileDb.save()


	#upload status
	uploadStatus(at,2,"running","-")
	return True

def downloadHistory(driveService,at):
	""" Download the history for a file """

	meta = getMetaData(at)

	downDir = Download.objects.get(tokenID=at).folder
	downDirFull = os.path.join(settings.DOWNLOAD_DIR,downDir)
	downDirHistory = os.path.join(downDirFull,"history")

	#create the directories if necessary
	if not os.path.isdir(downDirFull):
		os.mkdir(downDirFull)

	if not os.path.isdir(downDirHistory):
		os.mkdir(downDirHistory)

	for item in meta['items']:
		try:
			#get revisions for this file
			revs = driveService.revisions().list(fileId=item['id']).execute()

			# if len == 1 we do not have any revision
			if len(revs['items']) > 1:
				print len(revs['items'])

				#create a folder for this file
				revPath = os.path.join(downDirHistory,item['id'])
				if not os.path.isdir(revPath):
						os.mkdir(revPath)

				#download
				print item['title']
				print item['id']
				fileDownload = FileDownload.objects.filter(fileName=item['title'],alternateName=item['id'])
				for r in revs['items']:
					revItem = base64.b64encode(json.dumps(r))
					revID = r['id']
					#print revID

					if 'downloadUrl' in r:
						url = r['downloadUrl']
					elif 'exportLinks' in r:
						url = r['exportLinks']['application/pdf']

					resp, content = driveService._http.request(url)
					
					#if the response is affirmative
					if resp.status == 200:
						fullName = os.path.join(revPath,item['title']+"_"+revID)

						f = open(fullName,"wb+")
						f.write(content)
						f.close()

						fh = FileHistory(revision=revID,status=1,fileDownloadID=fileDownload[0],revisionMetadata=revItem)
						fh.save()
		except errors.HttpError, error:
			print error

	uploadStatus(at,3,"running","-")
	return True
