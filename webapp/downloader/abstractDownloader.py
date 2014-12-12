import abc,os
from django.conf import settings
from verifier import Verifier

class AbstractDownloader(object):
	__metaclass__ = abc.ABCMeta
	
	def __init__(self,download,uname,pwd):
		self.d = download
		self.t = download.tokenID
		self.service = None
		self.metadata = None
		self.metadataObject = None
		self.uname = uname
		self.pwd = pwd

		#set download dir
		downDir = os.path.join(settings.DOWNLOAD_DIR,download.folder)

		if not os.path.isdir(downDir):
			os.mkdir(downDir)

		self.downloadDir = downDir
		self.v = Verifier(self.d)
	
	def verfiyCredentials(self):
		status = self.v.verifyCredentials(self.uname,self.pwd)
		self.d.threadStatus = status
		self.d.save()

	def verificationProcess(self):
		status = self.v.verificationProcess()
		self.d.threadStatus = status
		self.d.save()

	@abc.abstractmethod
	def downloadFileHistory(self):
		return

	@abc.abstractmethod
	def createService(self):
		return

	@abc.abstractmethod
	def downloadMetaData(self):
		return

	@abc.abstractmethod
	def downloadFiles(self):
		return

	@abc.abstractmethod
	def downloadHistory(self):
		return

	@abc.abstractmethod
	def computeDownload(self):
		return

