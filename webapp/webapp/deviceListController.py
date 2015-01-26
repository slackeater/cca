import constConfig
from devicelister.googleDeviceLister import GoogleDeviceLister
from devicelister.dropboxDeviceLister import DropboxDeviceLister

class DeviceListController(object):

	def __init__(self,token,email,pwd):

		self.csp = None

		if token.serviceType == constConfig.CSP_GOOGLE:
			self.csp = GoogleDeviceLister(token,email,pwd)
		elif token.serviceType == constConfig.CSP_DROPBOX:
                        self.csp = DropboxDeviceLister(token,email,pwd)

	def listDevices(self):
		self.csp.connect()
		return self.csp.devList()
