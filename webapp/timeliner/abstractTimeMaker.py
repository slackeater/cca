import abc
from webapp.databaseInterface import DbInterface

class AbstractTimeMaker(object):
	__metaclass__ = abc.ABCMeta

	def __init__(self,token):
		self.ci = token.cloudItem
		self.t = token
		self.db = DbInterface()

	@abc.abstractmethod
	def constructTimeLineItem(self,item,isHistory = False):
		return

	@abc.abstractmethod
	def formTimeLine(self,resType,mimeType,startDate,endDate):
		return

	@abc.abstractmethod
	def filehistoryTimeLine(self,alternateName):
		return

