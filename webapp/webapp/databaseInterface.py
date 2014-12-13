from downloader.models import *
from dashboard.models import *
import json,base64


class DbInterface():

	def getToken(self,id):
		return AccessToken.objects.get(id=id)

	@staticmethod
	def getAccessTokenList(clouditem):
		return AccessToken.objects.filter(cloudItem=clouditem)

	def getMetadataParsed(self,token):
		m = FileMetadata.objects.get(tokenID=token)
		return json.loads(base64.b64decode(m.metadata))

	def getFileDownload(self,token,id):
		return FileDownload.objects.get(tokenID=token,alternateName=id)

	def getHistoryForFile(self,fileDownload):
		return FileHistory.objects.filter(fileDownloadID=fileDownload)
