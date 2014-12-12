import abc
from webapp.databaseInterface import DbInterface


class AbstractAnalyzer():

	__metaclass__ = abc.ABCMeta

	def __init__(self,token):
		self.db = DbInterface()
		self.t = token
		self.metadata = self.db.getMetadataParsed(token)

	@abc.abstractmethod
	def metadataAnalysis(self):
		return

	@abc.abstractmethod
	def metadataSearch(self,searchType,mimeType,startDate,endDate):
		return

	@abc.abstractmethod
	def fileInfo(self,fileId):
		return

	@abc.abstractmethod
	def fileHistory(self,fileObject):
		return
