from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register
from django.core.exceptions import MultipleObjectsReturned
import oauth, sys, dropbox
import json, base64
from models import DropboxToken, GoogleDriveToken
from importer.models import Upload
from apiclient.discovery import build
from django.template.loader import render_to_string
import httplib2


@dajaxice_register
def submitDropboxCode(request, code, impID):
	""" Submit the dropbox authorization code """
	return submitCode(request, code, impID, "dropbox")

@dajaxice_register
def submitGoogleCode(request, code, impID):
	""" Submit the dropbox authorization code """
	return submitCode(request, code, impID, "google")

def submitCode(request, code, impID, platform):
	""" Get the access code from the code """

	if not request.user.is_authenticated():
		sys.exit("Auth required")

	dajax = Dajax()
	eID = "#gStat" if platform == "google" else "#dStat"
	
	try:
		if code is None:
			raise Exception("Invalid code")

		if platform == "google":
			credentials = oauth.googleAccessToken(code)
			http = httplib2.Http()
			http = credentials.authorize(http)

			#get user id
			user_info_service = build(serviceName='oauth2',version='v2',http=http)
			user_info = user_info_service.userinfo().get().execute()

			table = insertToken("google",user_info.get('id'), base64.b64encode(credentials.to_json()),impID)
			dajax.assign("#googleTokenTable", "innerHTML", table)
			dajax.assign(eID,"innerHTML", str(""))
		elif platform == "dropbox":
			accessToken, userID = oauth.dropboxAccessToken(code)
			table = insertToken("dropbox",userID,accessToken, impID)
			dajax.assign("#dropTokenTable", "innerHTML", table)
			dajax.assign(eID,"innerHTML", str(""))
		else: 
			raise Exception("Invalid platform")

	except dropbox.rest.ErrorResponse as e:
		dajax.assign(eID,"innerHTML",str(e.status) + ", " + str(e.reason) + ", " + str(e.error_msg))
	except Exception as e:
		dajax.assign(eID,"innerHTML", str(e.message))
	
	return dajax.json()

def insertToken(platform, uid, token, importID):
	""" Insert a token into the relative table """

	if platform == "google":
		databaseModel = GoogleDriveToken
	elif platform == "dropbox":
		databaseModel = DropboxToken

	#check if we have already an access token for this id
	try:
		obj, created = databaseModel.objects.get_or_create(importID=Upload.objects.get(id=importID), userID=uid, defaults={'accessToken': token})

		if not created:
			obj.accessToken = token
			obj.save()

	except MultipleObjectsReturned:
		return None
	
	data = dict()
	data['tknTable'] = databaseModel.objects.all()
	data['link'] = "gdrivecloud" if platform == "google" else "dropcloud"
	data['objID'] = importID
	
	table = render_to_string("dashboard/tokenTable.html",data)
	return table

