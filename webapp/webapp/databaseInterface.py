from downloader.models import *
from dashboard.models import *
import json,base64


class DbInterface():

	@staticmethod
	def getToken(id):
		return AccessToken.objects.get(id=id)

	@staticmethod
	def getAccessTokenList(clouditem):
		return AccessToken.objects.filter(cloudItem=clouditem)

	def getMetadataParsed(self,token):
		m = FileMetadata.objects.get(tokenID=token)
		return json.loads(base64.b64decode(m.metadata))

	@staticmethod
	def getDownload(token):
		return Download.objects.get(tokenID=token)

	@staticmethod
	def getAllFileDownload(token):
		return FileDownload.objects.filter(tokenID=token)

	def getFileDownload(self,token,id):
		return FileDownload.objects.get(tokenID=token,alternateName=id)

	@staticmethod
	def getHistoryForFile(fileDownload):
		return FileHistory.objects.filter(fileDownloadID=fileDownload)
