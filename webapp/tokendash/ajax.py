from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register
from django.core.exceptions import MultipleObjectsReturned
import oauth, sys, dropbox
import json, base64
from downloader.models import AccessToken,Download
from importer.models import Upload
from apiclient.discovery import build
from django.template.loader import render_to_string
import httplib2
from django.utils.html import strip_tags
from webapp.func import *
from clouditem.models import CloudItem
from django.contrib.auth.models import User
from webapp import constConfig
from webapp.exceptionFormatter import formatException 
import math
from webapp.databaseInterface import DbInterface
from django.contrib.auth.decorators import login_required

@dajaxice_register
@login_required
def submitDropboxCode(request, code, ci):
	""" Submit the dropbox authorization code """
	return submitCode(request, code, ci, "dropbox","#dStat")

@dajaxice_register
@login_required
def submitGoogleCode(request, code, ci):
	""" Submit the dropbox authorization code """
	return submitCode(request, code, ci, "google","#gStat")

@dajaxice_register
@login_required
def showTokens(request,ci):
	""" Show the tokens """

	dajax = Dajax()

	try:
		data = dict()
		cloudItemObj = checkCloudItem(ci,request.user.id)
		data['tknTable'] = DbInterface.getAccessTokenList(cloudItemObj)
		data['id'] = cloudItemObj.id
		table = render_to_string("dashboard/tokenTable.html",data)
		dajax.assign("#tokenTable", "innerHTML", table)
		dajax.assign("#tokenError", "innerHTML","")
		dajax.add_css_class("#tokenError",[])
	except Exception as e:
		dajax.assign("#tokenError", "innerHTML",formatException(e))
		dajax.add_css_class("#tokenError",['alert','alert-danger'])

	return dajax.json()

def submitCode(request, code, ci, platform, eID):
	""" Get the access code from the code """


	dajax = Dajax()

	try:
		cloudItemID = parseAjaxParam(ci)
		code = strip_tags(code)

		if code is None:
			raise Exception("Invalid code")

		if platform == "google":
			credentials = oauth.googleAccessToken(code)
			http = httplib2.Http()
			http = credentials.authorize(http)

			#get user id
			user_info_service = build(serviceName='oauth2',version='v2',http=http)
			user_info = user_info_service.userinfo().get().execute()

			insertToken("google",user_info.get('id'), credentials.to_json(),cloudItemID,user_info)
			dajax.assign(eID,"innerHTML", "")
		elif platform == "dropbox":
			accessToken, userID = oauth.dropboxAccessToken(code)
			#get user info
			client = dropbox.client.DropboxClient(accessToken)
			insertToken("dropbox",userID,accessToken,cloudItemID,client.account_info())
			dajax.assign(eID,"innerHTML", "")
		else: 
			raise Exception("Invalid platform")

	except dropbox.rest.ErrorResponse as e:
		dajax.assign(eID,"innerHTML",str(e.status) + ", " + str(e.reason) + ", " + str(e.error_msg))
	except Exception as e:
		dajax.assign(eID,"innerHTML", str(e.message))
	
	return dajax.json()

def insertToken(platform, uid, token, cloudItemID,userInfo):
	""" Insert a token into the relative table """

	#check if we have already an access token for this id
	try:
		parseToken = base64.b64encode(token)
		parseInfo = base64.b64encode(json.dumps(userInfo))
		obj, created = AccessToken.objects.get_or_create(cloudItem=CloudItem.objects.get(id=cloudItemID), userID=uid, serviceType=platform,userInfo=parseInfo,  defaults={'accessToken': parseToken})

		if not created:
			obj.accessToken = parseToken
			obj.save()

	except MultipleObjectsReturned:
		return None
	

