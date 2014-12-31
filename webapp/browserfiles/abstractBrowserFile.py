import abc


class AbstractBrowserFile():
	""" This class represent an abstract file browser """

	__metaclass__ = abc.ABCMeta

	@abc.abstractmethod
	def constructTimeLineItem(self):
		""" Construct an item to be used in the timeline """
		return

	@abc.abstractmethod
	def generateTimeLine(self,historyFile):
		""" Generate a timeline """
		return
