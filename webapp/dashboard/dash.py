from importer.models import Upload
import os, json, oauth
from django.template.loader import render_to_string
from models import AccessToken
from django.conf import settings

def importViewer(importID):
	""" Manage the view of the reporter """
	up = Upload.objects.get(id=importID)
	data =  { 'up': up }

	jsonReport = getReportJson(up)
	data['attributes'] = jsonReport[0]['objects']
	data['browser'] = jsonReport[1]['objects']
	data['cloud'] = jsonReport[2]['objects']
	
	return data

def cloudDownloader(importID):
	""" Show the access token for the services """

	#get all credentials
	up = Upload.objects.get(id=importID)
	jsonReport = getReportJson(up)

	#to show the credentials
	browser = jsonReport[1]['objects']
	data = dict()
	data['dropAuthurl'] = oauth.dropboxAuthorizeURL()
	data["gdriveAuthurl"] = oauth.googleAuthorizeURL()
	
	# credentials
	data["browsers"] = browser

	return data
"""
def cloudService(request, service, tokenID, importID):

	#first, store credentials inside a session variable to avoid multiple db calls
	sessionCred = request.session.get(sessionName, "none")
	sessionName = SESSION_NAME+str(importID)+"-"+str(tokenID)

	if sessionCred == "none":
		try:
			dbObject = GoogleDriveToken if service == "google" elif service == "dropbox" DropboxToken else ""

			token = dbObject.objects.get(importID=Upload.objects.get(id=importID), id=tokenID)

			#store
			request.session[sessionName] = base64.b64decode(token.accessToken)
		except AccessToken.DoesNotExist:
			return redirect("/dashboard/?i="+str(importID)+"&s=cloud")

"""
def getReportJson(uploadObject):
	""" Read the JSON of the report """

	#get report content
	if uploadObject.fileName.endswith(".zip.enc"):
		name = uploadObject.fileName[:-8]
	else:
		raise Exception("Incorret import name")

	fileName = os.path.join(settings.UPLOAD_DIR, name, name+".report")
	openFile = open(fileName, "r")
	return json.load(openFile)
