from maps.googleMapper import GoogleMapper
from maps.dropboxMapper import DropboxMapper
import constConfig


class MapsController(object):


	def __init__(self,token):
		self.t = token
		self.csp = None

		#initialize the platform of the token
		if self.t.serviceType == constConfig.CSP_GOOGLE:
			self.csp = GoogleMapper(self.t)
		elif self.t.serviceType == constConfig.CSP_DROPBOX:
			self.csp = DropboxMapper(self.t)

	def findExif(self):
		return self.csp.findExif()

	def mailFinder(self):
		return self.csp.mailFinder()


