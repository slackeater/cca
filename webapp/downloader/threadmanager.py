import thread
import googleDownloader
from apiclient.discovery import build
import httplib2
from oauth2client.client import OAuth2Credentials
from models import AccessToken, Download
from clouditem.models import CloudItem
import json, base64

class ThreadManager:
	def __init__(self,tokenID):
		self.t = tokenID

	def download(self):
		#select platform
		at = AccessToken.objects.get(id=self.t)

		if at.serviceType == "google":
			
			#set status starting
			d = Download.objects.get(tokenID=at)
			d.status = 0
			d.save()
			
			#start download
			tup = (at,)
			thread.start_new_thread(self.googleDownload,tup)
		elif at.serviceType == "dropbox":
			#start dropbox download
			pass

	def makeGoogleService(self,serviceType,jsonCredentials):
		""" Create a google service """

		http = httplib2.Http()
		credentials = OAuth2Credentials.from_json(jsonCredentials)
		credAuth = credentials.authorize(http)
		return build(serviceType,"v2",credAuth)


	def googleDownload(self,accessToken):
		credentials = base64.b64decode(accessToken.accessToken)
		service = self.makeGoogleService("drive",credentials)
		googleDownloader.downloadMetaData(service,accessToken)
