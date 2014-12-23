from cloudservice.googledrive import GoogleAnalyzer
from cloudservice.drop import DropboxAnalyzer
import constConfig


class MetadataController(object):


	def __init__(self,token):
		self.t = token
		self.csp = None

		#initialize the platform of the token
		if self.t.serviceType == constConfig.CSP_GOOGLE:
			self.csp = GoogleAnalyzer(self.t)
		elif self.t.serviceType == constConfig.CSP_DROPBOX:
			self.csp = DropboxAnalyzer(self.t)


	def metadataAnalysis(self):
		return self.csp.metadataAnalysis()

	def metadataSearch(self,searchType,searchEmail,searchFile,searchGivenName,filterType,mimeType,startDate,endDate):
		return self.csp.metadataSearch(searchType,searchEmail,searchFile,searchGivenName,filterType,mimeType,startDate,endDate)

	def fileInfo(self,fileID):
		return self.csp.fileInfo(fileID)

	def fileHistory(self,fileObject):
		return self.csp.fileHistory(fileObject)
