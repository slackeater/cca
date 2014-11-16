import thread
import googleDownloader, dropDownloader
import dropbox
from apiclient.discovery import build
import httplib2
from oauth2client.client import OAuth2Credentials
from models import AccessToken, Download
from clouditem.models import CloudItem
import json, base64

class ThreadManager:
	""" Manage the thread for downloading data """
	def __init__(self,tokenID):
		self.t = tokenID

	def download(self):
		""" Start the thread """
		#select platform
		at = AccessToken.objects.get(id=self.t)

		#set status starting
		d = Download.objects.get(tokenID=at)
		d.status = 0
		d.threadStatus = "running"
		d.threadMessage = "Download is starting..."
		d.save()
		
		#thread param
		tup = (at,)

		if at.serviceType == "google":
			x = thread.start_new_thread(self.googleDownload,tup)
		elif at.serviceType == "dropbox":
			x = thread.start_new_thread(self.dropboxDownloader,tup)

	def makeGoogleService(self,serviceType,jsonCredentials):
		""" Create a google service """

		http = httplib2.Http()
		credentials = OAuth2Credentials.from_json(jsonCredentials)
		credAuth = credentials.authorize(http)
		return build(serviceType,"v2",credAuth)

	def makeDropboxService(self,accessTokenValue):
		""" Create a client for dropbox """

		c = dropbox.client.DropboxClient(accessTokenValue)
		return c

	def updateStatus(self,at,threadStatus,threadMessage,status = None):
		""" Update the status of the download """
		downloadItem = Download.objects.get(tokenID=at)

		if status != None:
			downloadItem.status = status

		downloadItem.threadStatus = threadStatus
		downloadItem.threadMessage = threadMessage
		downloadItem.save()

	def googleDownload(self,accessToken):
		""" Download sequence of google """
		try:
			credentials = base64.b64decode(accessToken.accessToken)
			service = self.makeGoogleService("drive",credentials)
			#download metadata
			thStatus, thMsg, status = googleDownloader.downloadMetaData(service,accessToken)
			self.updateStatus(accessToken,thStatus, thMsg, status)
			#download files
			thStatus, thMsg, status = googleDownloader.downloadFiles(service,accessToken)
			self.updateStatus(accessToken,thStatus, thMsg, status)
			#download history
			thStatus, thMsg, status = googleDownloader.downloadHistory(service,accessToken)
			self.updateStatus(accessToken,thStatus, thMsg, status)
		except httplib2.ServerNotFoundError as e:
			#update db
			self.updateStatus(accessToken,"stopped",e.message,None)
			return

	def dropboxDownloader(self, accessToken):
		""" Download sequence of dropbox """

		try:
			atValue = base64.b64decode(accessToken.accessToken)
			client = self.makeDropboxService(atValue)
			#metadata
			thStatus, thMsg , status = dropDownloader.downloadMetaData(client,accessToken)
			self.updateStatus(accessToken,thStatus, thMsg, status)
			#files
			thStatus, thMsg, status  = dropDownloader.downloadFiles(client,accessToken)
			self.updateStatus(accessToken,thStatus, thMsg, status)
			#history
			thStatus, thMsg, status = dropDownloader.downloadHistory(client, accessToken)
			self.updateStatus(accessToken,thStatus, thMsg, status)
		except dropbox.rest.ErrorResponse as e:
			self.updateStatus(accessToken,"stopped",e,None)
			return

