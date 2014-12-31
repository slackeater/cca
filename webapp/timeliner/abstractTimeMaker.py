import abc
from webapp.databaseInterface import DbInterface

class AbstractTimeMaker(object):
	""" This class represent an abstract time maker """

	__metaclass__ = abc.ABCMeta

	def __init__(self,token):
		self.ci = token.cloudItem
		self.t = token
		self.db = DbInterface()

	@abc.abstractmethod
	def constructTimeLineItem(self,item,isHistory = False):
		""" Construct an item that will be places in the timeline """
		return

	@abc.abstractmethod
	def formTimeLine(self,resType,mimeType,startDate,endDate):
		""" Construct the time line for files """
		return

	@abc.abstractmethod
	def filehistoryTimeLine(self,alternateName):
		""" Construct a time line for history """
		return

