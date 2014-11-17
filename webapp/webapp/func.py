import md5
from downloader.models import *
from clouditem.models import CloudItem
from django.contrib.auth.models import User


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
