import abc
from webapp.databaseInterface import DbInterface
from downloader.models import Download
from webapp import constConfig

class AbstractMaps():

	__metaclass__ = abc.ABCMeta

	def __init__(self,token):
		self.t = token
		self.d = Download.objects.get(tokenID=self.t,threadStatus=constConfig.THREAD_TS)
		self.db = DbInterface()
		self.metadata = self.db.getMetadataParsed(self.t)

	@abc.abstractmethod
	def findExif(self):
		return

	@abc.abstractmethod
	def mailFinder(self):
		return

