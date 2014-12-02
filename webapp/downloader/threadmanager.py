import threading
import googleDownloader, dropDownloader
import dropbox
from apiclient.discovery import build
import httplib2
from oauth2client.client import OAuth2Credentials
from models import AccessToken, Download
from clouditem.models import CloudItem
import json, base64
from webapp import constConfig

class ThreadManager:
	""" Manage the thread for downloading data """
	def __init__(self,tokenID,isTestThread = False):
		self.t = tokenID
		self.isTestThread = isTestThread
		self.statusList = list()

	def download(self):
		""" Start the thread """
		#select platform
		at = AccessToken.objects.get(id=self.t)

		#set status init
		self.updateStatus(at,constConfig.THREAD_INIT,"-")

		#thread param
		tup = (at,)

		if at.serviceType == "google":
			threadInstance = threading.Thread(target=self.googleDownload,args=tup)
			threadInstance.start()
			return threadInstance
		elif at.serviceType == "dropbox":
			threadInstance = threading.Thread(target=self.dropboxDownloader,args=tup)
			threadInstance.start()
			return threadInstance

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

	def updateStatus(self,at,threadStatus,threadMessage):
		""" Update the status of the download """
		downloadItem = Download.objects.get(tokenID=at)

		downloadItem.threadStatus = threadStatus
		downloadItem.threadMessage = threadMessage
		downloadItem.save()

		if self.isTestThread:
			self.statusList.append(downloadItem)

	def googleDownload(self,accessToken):
		""" Download sequence of google """

		try:
			self.updateStatus(accessToken,constConfig.THREAD_DOWN,"-")

			#update status to starting
			credentials = base64.b64decode(accessToken.accessToken)

			if self.isTestThread:
				service = None
			else: 
				service = self.makeGoogleService("drive",credentials)

			#download metadata
			status = googleDownloader.downloadMetaData(service,accessToken,self.isTestThread)
			self.updateStatus(accessToken,status, "-")

			#download files
			status = googleDownloader.downloadFiles(service,accessToken,self.isTestThread)
			self.updateStatus(accessToken,status, "-")

			#download history
			status = googleDownloader.downloadHistory(service,accessToken,self.isTestThread)
			self.updateStatus(accessToken,status, "-")

		except (Exception,httplib2.ServerNotFoundError) as e:
			#update db
			self.updateStatus(accessToken,constConfig.THREAD_STOP,e.message)
			return

	def dropboxDownloader(self, accessToken):
		""" Download sequence of dropbox """

		try:
			self.updateStatus(accessToken,constConfig.THREAD_DOWN,"-")

			atValue = base64.b64decode(accessToken.accessToken)

			if self.isTestThread:
				client = None
			else: 
				client = self.makeDropboxService(atValue)

			#metadata
			status = dropDownloader.downloadMetaData(client,accessToken,self.isTestThread)
			self.updateStatus(accessToken,status, "-")

			#files
			status  = dropDownloader.downloadFiles(client,accessToken,self.isTestThread)
			self.updateStatus(accessToken,status,"-")

			#history
			status = dropDownloader.downloadHistory(client, accessToken,self.isTestThread)
			self.updateStatus(accessToken,status,"-")

		except dropbox.rest.ErrorResponse as e:
			self.updateStatus(accessToken,constConfig.THREAD_STOP,e.message)
			return

