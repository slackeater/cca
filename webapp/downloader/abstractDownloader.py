import abc,os
from django.conf import settings
from verifier import DTAVerifier

class AbstractDownloader(object):
	""" An abstract class that represent a download """

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
		self.v = DTAVerifier(self.d)

	def computeFileSize(self,source):
		""" Compute the total size of downloaded files http://snipplr.com/view.php?codeview&id=47686 """
		total_size = os.path.getsize(source)

		for item in os.listdir(source):
			itempath = os.path.join(source, item)

			if os.path.isfile(itempath):
				total_size += os.path.getsize(itempath)
			elif os.path.isdir(itempath):
				total_size += self.computeFileSize(itempath)

		return total_size

	def verfiyCredentials(self):
		""" Verify the credentials of the timestamp service """
		status = self.v.verifyCredentials(self.uname,self.pwd)
		self.d.threadStatus = status
		self.d.save()

	def verificationProcess(self):
		""" Start the verfification process where we generate a timestamp """
		status = self.v.verificationProcess()
		self.d.threadStatus = status
		self.d.save()

	@abc.abstractmethod
	def downloadFileHistory(self):
		""" Wrapper for the download of the files and history of the files """
		return

	@abc.abstractmethod
	def createService(self):
		""" Create the service of the cloud provider with its API """
		return

	@abc.abstractmethod
	def downloadMetaData(self):
		""" Download the metadata of the account """
		return

	@abc.abstractmethod
	def downloadFiles(self):
		""" Download the files of the account """
		return

	@abc.abstractmethod
	def downloadHistory(self):
		""" Download the history of the files """
		return

	@abc.abstractmethod
	def computeDownload(self):
		""" Compute the download size """
		return

