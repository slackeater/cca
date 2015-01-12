import constConfig, os,sys
from browserfiles.chromeBrowserFile import GoogleChromeFiles
from browserfiles.firefoxBrowserFile import FirefoxFiles
from importer.models import Upload
from django.conf import settings
from webapp import crypto
from webapp.func import getTimestamp


class BrowserFileController(object):


	def __init__(self,cloudItem,browserParam):

		self.fb = None

		#check that an import exists
		imp = Upload.objects.get(cloudItemID=cloudItem)

		#compute import path
		importPath = crypto.sha256(imp.fileName+crypto.HASH_SEPARATOR+getTimestamp(imp.uploadDate)).hexdigest()

		self.filePath = os.path.join(settings.UPLOAD_DIR,str(cloudItem.id),importPath,imp.fileName)
		
		profile = str(browserParam.split("_",1)[1])
	
		#windows profile are stored with Profile\in front
		if profile.startswith("Profile"):
			profile = profile[9:]

		if int(browserParam[0]) == constConfig.HISTORY_FORM_CHROME:
			self.fb = GoogleChromeFiles(self.filePath,profile)
		elif int(browserParam[0]) == constConfig.HISTORY_FORM_FF:
			self.fb = FirefoxFiles(self.filePath,profile)
				


	def generateTimeLine(self,domain):
		return self.fb.generateTimeLine(domain)
