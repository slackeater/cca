from clouditem.models import CloudItem
from downloader.models import AccessToken, FileMetadata, FileDownload, FileHistory
from dashboard.models import MimeType
from django.contrib.auth.models import User
from django.conf import settings
import json,os

class MakeDatabase():

	filePath = os.path.join(settings.BASE_DIR,"webapp","tests")

	def populate(self):

		# === create a user
		self.createUser()
		# === create a cloud item
		self.createCloudItem()
		# === create access tokens
		self.createAccessToken()
		# === create file metadata 
		self.createFileMetadata()
		# === create file download
		self.createFileDownload()
		# === create file history
		self.createFileHistory()
		# === create mime type db
		self.createMimeType()

	def createUser(self):
		User.objects.create_user(username="reporter",password='reporter',email="rep@rep.com")

	def createCloudItem(self):
		user = User.objects.all()[0]
		ci = CloudItem(desc="Set up clouditem",reportName="Set up",reporterID=user)
		ci.save()
	
	def createAccessToken(self):
		ci = CloudItem.objects.all()[0]
		atPath = os.path.join(self.filePath,"downloader_accesstoken.json")
		atData = json.load(open(atPath,"rb"))

		for a in atData:
			at = AccessToken(id=a['id'],accessToken=a['accessToken'],userID=a['userID'],serviceType=a['serviceType'],tokenTime=a['tokenTime'],userInfo=a['userInfo'],
					cloudItem=ci)
			at.save()

	def createFileMetadata(self):
		fmPath = os.path.join(self.filePath,"downloader_filemetadata.json")
		fmData = json.load(open(fmPath,"rb"))
	
		# create db data
		for r in fmData:
			f = FileMetadata(id=r['id'],metadata=r['metadata'],metaTime=r['metaTime'],tokenID=AccessToken.objects.get(id=r['tokenID_id']))
			f.save()


	def createMimeType(self):
		mimePath = os.path.join(self.filePath,"dashboard_mimetype.json")
		mimeData = json.load(open(mimePath,"rb"))

		for m in mimeData:
			mime = MimeType(id=m['id'],mime=m['mime'])
			mime.save()	

	def createFileDownload(self):
		fdPath = os.path.join(self.filePath,"downloader_filedownload.json")
		fdData = json.load(open(fdPath,"rb"))

		for fd in fdData:
			fileDown = FileDownload(id=fd['id'],fileName=fd['fileName'],alternateName=fd['alternateName'],status=fd['status'],downloadTime=fd['downloadTime'],
					tokenID=AccessToken.objects.get(id=fd['tokenID_id']))
			fileDown.save()

	def createFileHistory(self):
		fhPath = os.path.join(self.filePath,"downloader_filehistory.json")
		fhData = json.load(open(fhPath,"rb"))

		for fd in fhData:
			fileHist = FileHistory(id=fd['id'],revision=fd['revision'],status=fd['status'],fileDownloadID=FileDownload.objects.get(id=fd['fileDownloadID_id']),revisionMetadata=fd['revisionMetadata'])
			fileHist.save()
