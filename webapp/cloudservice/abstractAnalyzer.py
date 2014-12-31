import abc
from webapp.databaseInterface import DbInterface


class AbstractAnalyzer():
	""" This class represent an abstract analyzer """

	__metaclass__ = abc.ABCMeta

	def __init__(self,token):
		self.db = DbInterface()
		self.t = token
		self.metadata = self.db.getMetadataParsed(token)

	@abc.abstractmethod
	def metadataAnalysis(self):
		""" Display the stats about metadata """
		return

	@abc.abstractmethod
	def metadataSearch(self,searchType,mimeType,startDate,endDate):
		""" Search through the metadata """
		return

	@abc.abstractmethod
	def fileInfo(self,fileId):
		""" Display single file information """
		return

	@abc.abstractmethod
	def fileHistory(self,fileObject):
		""" Display file history """
		return
