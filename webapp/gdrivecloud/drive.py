from dashboard.models import GoogleDriveToken 
from importer.models import Upload
from oauth2client.client import OAuth2Credentials
import base64, sys, httplib2
from apiclient.discovery import build
from models import GoogleAccountInfo

def retrieveCredentials(request, importIDget, tokenID, sessioName):
	""" Retrieve the credentials from the db """

	#check if a session with credentials has been already created
	sessionCred = request.session.get(sessioName, "none") 

	if sessionCred != "none":
		#we already have this variable set
		return None

	# we have all the parameters
	if importIDget != 0 and tokenID != 0:
		try:
			token = GoogleDriveToken.objects.get(importID=Upload.objects.get(id=importIDget), id=tokenID)
		
			# create credentials
			request.session[sessioName] = base64.b64decode(token.accessToken)
		except GoogleDriveToken.DoesNotExist:
			raise Exception("Invalid parameters")	

def serviceBuilder(serviceName, version, httpObj):
	""" Create a service used to perform future API calls """
	return build(serviceName, version, httpObj)

def httpCreator(sessioName, credentialSession):
	""" Create an HTTP object to be passed to a build service """

	http = httplib2.Http()
	
	#get credentials 
	credentials = OAuth2Credentials.from_json(credentialSession)

	return credentials.authorize(http)
