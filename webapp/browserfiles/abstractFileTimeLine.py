import abc


class AbstractFileTimeLine():
	__metaclass__ = abc.ABCMeta

	def __init__(self,historyFile,cookieFile):
		self.h = historyFile
		self.c = cookieFile

	@abc.abstractmethod
	def constructTimeLineItem(self):
		return

	@abc.abstractmethod
	def generateTimeLine(self):
		return
