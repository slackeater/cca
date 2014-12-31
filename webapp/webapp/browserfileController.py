import constConfig, os,sys
from browserfiles.chromeBrowserFile import GoogleChromeFiles
from importer.models import Upload
from django.conf import settings

cryptoPath = os.path.join(os.path.dirname(settings.BASE_DIR), "finder")

if not cryptoPath in sys.path:
	sys.path.insert(1, cryptoPath)
del cryptoPath

import crypto
from webapp.func import getTimestamp


class BrowserFileController(object):


	def __init__(self,cloudItem,browserParam):

		self.fb = None

		#check that an import exists
		imp = Upload.objects.get(cloudItemID=cloudItem)

		#compute import path
		importPath = crypto.sha256(imp.fileName+crypto.HASH_SEPARATOR+getTimestamp(imp.uploadDate)).hexdigest()

		self.filePath = os.path.join(settings.UPLOAD_DIR,str(cloudItem.id),importPath,imp.fileName)

		if int(browserParam[0]) == constConfig.HISTORY_FORM_CHROME:
			self.fb = GoogleChromeFiles(self.filePath,browserParam.split("_",1)[1])

	def generateTimeLine(self,domain):
		return self.fb.generateTimeLine(domain)
