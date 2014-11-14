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
			x = thread.start_new_thread(self.googleDownload,tup)
			print "TH"
			print x
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
		try:
			credentials = base64.b64decode(accessToken.accessToken)
			service = self.makeGoogleService("drive",credentials)
			#download metadata
			#googleDownloader.downloadMetaData(service,accessToken)
			#download files
			#googleDownloader.downloadFiles(service,accessToken)
			#download history
			googleDownloader.downloadHistory(service,accessToken)
		except httplib2.ServerNotFoundError as e:
			#update db
			d = Download.objects.get(tokenID=accessToken)
			d.threadStatus = "stopped"
			d.threadMessage = e.message
			d.save()
			return
