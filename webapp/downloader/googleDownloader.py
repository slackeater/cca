from models import AccessToken,FileDownload,FileMetadata,FileHistory,Download
import base64,json,os
from django.conf import settings

def getMetaData(at):
	""" Get the metadata """
	m = json.loads(base64.b64decode(FileMetadata.objects.filter(tokenID=at)))
	return m

def uploadStatus(at,status,threadStatus,threadMessage):
	downloadItem = Download.objects.get(tokenID=at)
	
	#metadata downloaded and stored
	downloadItem.status = 1
	downloadItem.threadStatus = "running"
	downloadItem.threadMessage = "-"
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
	downDirFull = os.path.join(settings.DOWNLOAD_DIR,downDir,"files")

	#create directory if necessary
	if not os.path.isdir(downDirFull):
		os.mkdir(downDirFull)

	#iterate over file and write to disk
	for item in meta['items']:
		if item['downloadURL']:
			resp, content = driveService._http.request(item['downloadURL'])

			if resp.status == 200:
				fullName = os.path.join(downDirFull,item['title'] + "_" + item['id'])

				f = open(fullName,"rb")
				f.write(content)
				f.close()

				fileDb = FileDownload(fileName=item['title'],alternateName=item['id'],status=1,tokenID=at)
				fileDb.save()


	#upload status
	uploadStatus(at,2,"running","-")
	return True

def downloadHistory(driveService,at):
	""" Download the history for a file """
	pass
