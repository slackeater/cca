import constConfig
from timeliner.googletimemake import GoogleTimeMaker
from timeliner.droptimemaker import DropboxTimeMaker

class TimelinerController(object):


	def __init__(self,token):

		self.csp = None

		if token.serviceType == constConfig.CSP_GOOGLE:
			self.csp = GoogleTimeMaker(token)
		elif token.serviceType == constConfig.CSP_DROPBOX:
			self.csp = DropboxTimeMaker(token)

	def formTimeLine(self,formType,searchEmail,searchFilename,searchGivenName,resType,mimeType,startDate,endDate):
		return self.csp.formTimeLine(formType,searchEmail,searchFilename,searchGivenName,resType,mimeType,startDate,endDate)

	def fileHistoryTimeLine(self,alternateName):
		return self.csp.filehistoryTimeLine(alternateName)

