from models import AccessToken,FileDownload,FileMetadata,FileHistory,Download
import base64,json

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

		#now update download status
		downloadItem = Download.objects.get(tokenID=at)
		
		#metadata downloaded and stored
		downloadItem.status = 1
		downloadItem.threadStatus = "running"
		downloadItem.save()

		return True
