from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register
from django.core.exceptions import MultipleObjectsReturned
import oauth, sys, dropbox
import json, base64
from webapp.func import *
from downloader.models import AccessToken
from importer.models import Upload
from apiclient.discovery import build
from django.template.loader import render_to_string
import httplib2
from django.utils.html import strip_tags
from oauth2client.client import FlowExchangeError

@dajaxice_register
def submitDropboxCode(request, code, impID):
	""" Submit the dropbox authorization code """
	stripCode = strip_tags(code)
	return submitCode(request, stripCode, impID, "dropbox","#dStat")

@dajaxice_register
def submitGoogleCode(request, code, impID):
	""" Submit the dropbox authorization code """
	stripCode = strip_tags(code)
	return submitCode(request, stripCode, impID, "google","#gStat")

@dajaxice_register
def showTokens(request, platform, impID):
	""" Show the tokens """

	if not isAuthenticated(request):
		return None
	
	dajax = Dajax()

	cleanPlatform = strip_tags(platform)	

	if cleanPlatform == "google":
		eID = "#gStat"
		tab = "#googleTokenTable"
	elif cleanPlatform == "dropbox":
		eID = "#dStat"
		tab = "#dropTokenTable"
	
	try:	
		data = dict()
		data['tknTable'] = AccessToken.objects.filter(serviceType=cleanPlatform)
		data['link'] = cleanPlatform
		data['id'] = parseAjaxParam(impID)
		table = render_to_string("dashboard/tokenTable.html",data)
		dajax.assign(tab, "innerHTML", table)
	except Exception as e:
		dajax.assign(eID, "innetHTML", e.message)

	return dajax.json()

def submitCode(request, code, impID, platform,eID):
	""" Get the access code from the code """

	if not isAuthenticated(request):
		return None

	dajax = Dajax()
	
	try:
		if code is None or len(code) < 10:
			raise Exception("Invalid code")

		if platform == "google":
			#build an http object 
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
	except FlowExchangeError as e:
		dajax.assign(eID,"innerHTML",str(e))
	except Exception as e:
		dajax.assign(eID,"innerHTML", str(e.message))
	
	return dajax.json()

def insertToken(platform, uid, token, importID):
	""" Insert a token into the relative table """

	parseToken = base64.b64encode(token)
	obj, created = AccessToken.objects.get_or_create(importID=Upload.objects.get(id=importID), userID=uid, serviceType=platform,  defaults={'accessToken': parseToken})

	if not created:
		obj.accessToken = parseToken
		obj.save()
	

