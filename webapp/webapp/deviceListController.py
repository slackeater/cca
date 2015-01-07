import constConfig
from devicelister.googleDeviceLister import GoogleDeviceLister

class DeviceListController(object):

	def __init__(self,token,email,pwd):

		self.csp = None

		if token.serviceType == constConfig.CSP_GOOGLE:
			self.csp = GoogleDeviceLister(token,email,pwd)
		elif token.serviceType == constConfig.CSP_DROPBOX:
			pass

	def listDevices(self):
		self.csp.connect()
		return self.csp.devList()
