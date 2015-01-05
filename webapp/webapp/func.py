import md5,os,sys,json,base64
from django.conf import settings
from downloader.models import *
from importer.models import Upload
from clouditem.models import CloudItem
from django.contrib.auth.models import User
from django.utils.dateformat import format
from django.core.exceptions import ObjectDoesNotExist

# add path for crypto
cryptoPath = os.path.join(os.path.dirname(settings.BASE_DIR), "finder")

if not cryptoPath in sys.path:
	sys.path.insert(1, cryptoPath)
	del cryptoPath

import crypto

def dataDecoder(data):
	""" Decode the data stored in the Db previously encoded with JSON + Base64 """
	return json.loads(base64.b64decode(data))

def isAuthenticated(request):
	""" Check if a user is authenticated """
	if request.user.is_authenticated():
		return True

	return False

def parseAjaxParam(param):
	""" Force a cast to int of get parameters """
	return int(param)

def sessionName(identifier):
	""" Return a session name for a give identifer """
	return md5.new(str(identifier)).hexdigest()

def dropboxAlternateName(path,modified):
	""" Return the alternate name for dropbox files """
	return md5.new(path.encode("utf-8")+modified.encode("utf-8")).hexdigest()

def checkCloudItem(cloudItemID,userID):
	""" Check if a cloud item belongs to the user logged in """

	ciFromUser = CloudItem.objects.get(id=cloudItemID,reporterID=User.objects.get(id=userID))
	return ciFromUser

def checkAccessToken(tokenID,cloudItemObj):
	""" Check that a token belongs to the current clouditem """

	tknFromCi = AccessToken.objects.get(id=tokenID,cloudItem=cloudItemObj)
	return tknFromCi

def openReport(clouditem,uploadID = None):

	try:
		# get the upload
		if uploadID is not None:
			uploadQuery = Upload.objects.get(cloudItemID=clouditem,id=uploadID)
		else:
			uploadQuery = Upload.objects.get(cloudItemID=clouditem)

		#build the name of the folder
		hashFolder = crypto.sha256(uploadQuery.fileName+crypto.HASH_SEPARATOR+format(uploadQuery.uploadDate,"U")).hexdigest()

		#parse with JSON
		report = os.path.join(settings.UPLOAD_DIR,str(clouditem.id),hashFolder,uploadQuery.fileName,uploadQuery.fileName+".report")

		openReport = open(report,"rb")
		jsonReport = json.load(openReport)

		return jsonReport
	except ObjectDoesNotExist:
		return None


def getTimestamp(date):
	return format(date,"U")
