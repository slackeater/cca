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
from verifier import Verifier
from webapp.exceptionFormatter import formatException

class ThreadManager:
	""" Manage the thread for downloading data """
	def __init__(self,tokenID,isTestThread = False):
		self.t = AccessToken.objects.get(id=tokenID)
		self.isTestThread = isTestThread
		self.statusList = list()
		self.v = Verifier(self.t)

	def download(self,uname,pwd):
		""" Start the thread """
		#verify credentials
		if self.isTestThread is False:
			self.v.verifyCredentials(uname,pwd)

		#set status init
		self.updateStatus(constConfig.THREAD_INIT,"-")

		if self.t.serviceType == "google":
			threadInstance = threading.Thread(target=self.googleDownload)
			threadInstance.start()
			return threadInstance
		elif self.t.serviceType == "dropbox":
			threadInstance = threading.Thread(target=self.dropboxDownloader)
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

	def updateStatus(self,threadStatus,threadMessage):
		""" Update the status of the download """
		downloadItem = Download.objects.get(tokenID=self.t)

		downloadItem.threadStatus = threadStatus
		downloadItem.threadMessage = threadMessage
		downloadItem.save()

		if self.isTestThread:
			self.statusList.append(downloadItem,formatException(e))

	def googleDownload(self):
		""" Download sequence of google """

		try:
			self.updateStatus(constConfig.THREAD_DOWN,"-")

			#update status to starting
			credentials = base64.b64decode(self.t.accessToken)

			if self.isTestThread:
				service = None
			else: 
				service = self.makeGoogleService("drive",credentials)

			#download metadata
			#status = googleDownloader.downloadMetaData(service,self.t,self.isTestThread)
			#self.updateStatus(status, "-")
			self.updateStatus(constConfig.THREAD_PHASE_1, "-")

			#download files
			#status = googleDownloader.downloadFiles(service,self.t,self.isTestThread)
			self.updateStatus(constConfig.THREAD_PHASE_2, "-")

			#download history
			#status = googleDownloader.downloadHistory(service,self.t,self.isTestThread)
			self.updateStatus(constConfig.THREAD_PHASE_3, "-")
					
			#create verification ZIP
			self.v.verificationProcess()

		except (Exception,httplib2.ServerNotFoundError) as e:
			#update db
			self.updateStatus(constConfig.THREAD_STOP,formatException(e))
			return

	def dropboxDownloader(self):
		""" Download sequence of dropbox """

		try:
			self.updateStatus(constConfig.THREAD_DOWN,"-")

			atValue = base64.b64decode(self.t.accessToken)

			if self.isTestThread:
				client = None
			else: 
				client = self.makeDropboxService(atValue)

			#metadata
			status = dropDownloader.downloadMetaData(client,self.t,self.isTestThread)
			self.updateStatus(status, "-")

			#files
			status  = dropDownloader.downloadFiles(client,self.t,self.isTestThread)
			self.updateStatus(status,"-")

			#history
			status = dropDownloader.downloadHistory(client,self.t,self.isTestThread)
			self.updateStatus(status,"-")

		except (Exception,dropbox.rest.ErrorResponse) as e:
			self.updateStatus(constConfig.THREAD_STOP,formatException(e))
			return

