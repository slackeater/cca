from clouditem.models import CloudItem
from downloader.models import AccessToken, FileMetadata, FileDownload, FileHistory,Download
from dashboard.models import MimeType
from django.contrib.auth.models import User
from django.conf import settings
import json,os,time,datetime,pytz
from django.utils import timezone

class MakeDatabase():

	filePath = os.path.join(settings.BASE_DIR,"webapp","tests")

	def makeDate(self,dateStr):
		date = list(time.strptime(dateStr,"%Y-%m-%d %H:%M:%S"))[:6]
		tzDate = timezone.datetime(date[0],date[1],date[2],date[3],date[4],date[5])
		return tzDate

	def populate(self):

		# === create a user
		self.createUser()
		# === create a cloud item
		self.createCloudItem()
		# === create access tokens
		self.createAccessToken()
		# === create download
		self.createDownload()
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
		ciPath = os.path.join(self.filePath,"clouditem_clouditem.json")
		ciData = json.load(open(ciPath,"rb"))
		
		for c in ciData:
			date = list(time.strptime(c['itemTime'],"%Y-%m-%d %H:%M:%S"))[:6]
			tzDate = pytz.utc.localize(timezone.datetime(date[0],date[1],date[2],date[3],date[4],date[5]))
			ci = CloudItem(id=c['id'],desc=c['desc'],reportName=c['reportName'],itemTime=tzDate,reporterID=user)
			ci.save()
	
	def createAccessToken(self):
		atPath = os.path.join(self.filePath,"downloader_accesstoken.json")
		atData = json.load(open(atPath,"rb"))

		for a in atData:
			date = list(time.strptime(a['tokenTime'],"%Y-%m-%d %H:%M:%S"))[:6]
			tzDate = pytz.utc.localize(timezone.datetime(date[0],date[1],date[2],date[3],date[4],date[5]))
			at = AccessToken(id=a['id'],accessToken=a['accessToken'],userID=a['userID'],serviceType=a['serviceType'],tokenTime=tzDate,userInfo=a['userInfo'],
					cloudItem=CloudItem.objects.get(id=a['cloudItem_id']))
			at.save()

	def createFileMetadata(self):
		fmPath = os.path.join(self.filePath,"downloader_filemetadata.json")
		fmData = json.load(open(fmPath,"rb"))
	
		# create db data
		for r in fmData:
			date = list(time.strptime(r['metaTime'],"%Y-%m-%d %H:%M:%S"))[:6]
			tzDate = pytz.utc.localize(datetime.datetime(date[0],date[1],date[2],date[3],date[4],date[5]))
			f = FileMetadata(id=r['id'],metadata=r['metadata'],metaTime=tzDate,tokenID=AccessToken.objects.get(id=r['tokenID_id']),metadataHash=r['metadataHash'])
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
			date = list(time.strptime(fd['downloadTime'],"%Y-%m-%d %H:%M:%S"))[:6]
			tzDate = pytz.utc.localize(datetime.datetime(date[0],date[1],date[2],date[3],date[4],date[5]))
			fileDown = FileDownload(id=fd['id'],fileName=fd['fileName'],alternateName=fd['alternateName'],fileHash=fd['fileHash'],status=fd['status'],downloadTime=tzDate,tokenID=AccessToken.objects.get(id=fd['tokenID_id']))
			fileDown.save()

	def createFileHistory(self):
		fhPath = os.path.join(self.filePath,"downloader_filehistory.json")
		fhData = json.load(open(fhPath,"rb"))

		for fd in fhData:
			date = list(time.strptime(fd['downloadTime'],"%Y-%m-%d %H:%M:%S"))[:6]
			tzDate = pytz.utc.localize(datetime.datetime(date[0],date[1],date[2],date[3],date[4],date[5]))
			fileHist = FileHistory(id=fd['id'],revision=fd['revision'],status=fd['status'],fileDownloadID=FileDownload.objects.get(id=fd['fileDownloadID_id']),revisionMetadata=fd['revisionMetadata'],fileRevisionHash=fd['fileRevisionHash'],revisionMetadataHash=fd['revisionMetadataHash'],downloadTime=tzDate)
			fileHist.save()

	def createDownload(self):
		dwPath = os.path.join(self.filePath,"downloader_download.json")
		dwData = json.load(open(dwPath,"rb"))

		for d in dwData:
			date = list(time.strptime(d['downTime'],"%Y-%m-%d %H:%M:%S"))[:6]
			tzDate = pytz.utc.localize(datetime.datetime(date[0],date[1],date[2],date[3],date[4],date[5]))
			dwItem = Download(id=d['id'],tokenID=AccessToken.objects.get(id=d['tokenID_id']),folder=d['folder'],downTime=tzDate,threadStatus=d['threadStatus'],threadMessage=d['threadMessage'],verificationZIP=d['verificationZIP'],verificationZIPSignature=d['verificationZIPSignature'],verificationZIPSignatureHash=d['verificationZIPSignatureHash'],verified=d['verified'])
			dwItem.save()

