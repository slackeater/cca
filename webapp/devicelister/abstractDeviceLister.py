import abc


class AbstractDeviceLister():
	""" This class represent an abstract file browser """

	__metaclass__ = abc.ABCMeta

	def __init__(self,token,email,pwd):
		self.email = email
		self.pwd = pwd
		self.t = token

	@abc.abstractmethod
	def connect(self):
		""" Connect to the CSP with the given credentials """
		return

	@abc.abstractmethod
	def devList(self):
		""" Return a list of the found devices """
		return
