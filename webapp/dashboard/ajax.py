from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register
from django.core.exceptions import MultipleObjectsReturned
import oauth, sys, dropbox
import json, base64
from models import AccessToken
from importer.models import Upload
from apiclient.discovery import build
from django.template.loader import render_to_string
import httplib2
from django.utils.html import strip_tags

@dajaxice_register
def submitDropboxCode(request, code, impID):
	""" Submit the dropbox authorization code """
	stripCode = strip_tags(code)
	return submitCode(request, stripCode, impID, "dropbox")

@dajaxice_register
def submitGoogleCode(request, code, impID):
	""" Submit the dropbox authorization code """
	stripCode = strip_tags(code)
	return submitCode(request, stripCode, impID, "google")

@dajaxice_register
def showTokens(request, platform, impID):
	""" Show the tokens """

	if not request.user.is_authenticated():
		return None

	importIDget = int(impID)
	
	if not importIDget > 0:
		return None

	dajax = Dajax()
	cleanPlatform = strip_tags(platform)	
	data = dict()

	if platform == "google":
		eID = "#gStat"
		tab = "#googleTokenTable"
	elif platform == "dropbox":
		eID = "#dStat"
		tab = "#dropTokenTable"

	try:	
		data['tknTable'] = AccessToken.objects.filter(serviceType=cleanPlatform)
		data['link'] = cleanPlatform
		data['id'] = importIDget
		table = render_to_string("dashboard/tokenTable.html",data)
		dajax.assign(tab, "innerHTML", table)
	except Exception as e:
		dajax.assign(eID, "innetHTML", e)

	return dajax.json()

def submitCode(request, code, impID, platform):
	""" Get the access code from the code """

	if not request.user.is_authenticated():
		return None

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

			insertToken("google",user_info.get('id'), credentials.to_json(),impID)
			dajax.assign(eID,"innerHTML", str(""))
		elif platform == "dropbox":
			accessToken, userID = oauth.dropboxAccessToken(code)
			insertToken("dropbox",userID,accessToken, impID)
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

	#check if we have already an access token for this id
	try:
		parseToken = base64.b64encode(token)
		obj, created = AccessToken.objects.get_or_create(importID=Upload.objects.get(id=importID), userID=uid, serviceType=platform,  defaults={'accessToken': parseToken})

		if not created:
			obj.accessToken = parseToken
			obj.save()

	except MultipleObjectsReturned:
		return None
	

