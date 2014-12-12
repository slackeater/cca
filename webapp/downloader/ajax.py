from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register
from django.core.exceptions import MultipleObjectsReturned
import oauth, sys, dropbox
import json, base64
from models import AccessToken,Download
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

@dajaxice_register
def submitDropboxCode(request, code, ci):
	""" Submit the dropbox authorization code """
	return submitCode(request, code, ci, "dropbox","#dStat")

@dajaxice_register
def submitGoogleCode(request, code, ci):
	""" Submit the dropbox authorization code """
	return submitCode(request, code, ci, "google","#gStat")

@dajaxice_register
def showGoogleTokens(request, ci):
	""" Show the token for google """
	return showTokens(request,"google",ci,"#gStat","#googleTokenTable")

@dajaxice_register
def showDropboxTokens(request, ci):
	""" Show the token for dropbox """
	return showTokens(request,"dropbox",ci,"#dStat","#dropTokenTable")

@dajaxice_register
def checkDownload(request,t,i):

	if not isAuthenticated(request):
		return None

	tokenID = parseAjaxParam(t)

	dajax = Dajax()

	try:
		cloudItem  = checkCloudItem(i,request.user.id)
		tokenQuery = checkAccessToken(t,cloudItem)

		downloadToken = Download.objects.get(tokenID=tokenQuery)

		#check the status
		s = downloadToken.threadStatus
		dajax.assign("#thStatus","innerHTML",s)	
		dajax.assign("#thMessage","innerHTML",downloadToken.threadMessage)	

		if s != constConfig.THREAD_NOTCLICKED and s != constConfig.THREAD_STOP:
			mask = {constConfig.THREAD_VERIFY_CRED: False, constConfig.THREAD_DOWN_META: False, constConfig.THREAD_COMPUTING: False,constConfig.THREAD_DOWN_FH: False, constConfig.THREAD_TS: False}

			#set the icons that have to use accept.png
			for key,value in mask.iteritems():
				if key <= s:
					mask[key] = True


			#now that states for icon are set, assign to dajax
			for key,value in mask.iteritems():
				if value is True:
					dajax.assign("#status"+str(key),"innerHTML","<img src='/static/icons/accept.png' />")

					if key >= 3:
						computeSize = float(downloadToken.downloadSize)/math.pow(2,20)
						dajax.assign("#fileSize","innerHTML",computeSize)
				else: 
					dajax.assign("#status"+str(key),"innerHTML","<img src='/static/loadersmall.gif' />")

		dajax.assign("#errors","innerHTML","")

	except Exception as e:
		dajax.assign("#errors","innerHTML",formatException(e))
	
	return dajax.json()

def showTokens(request, platform, ci, eID, tab):
	""" Show the tokens """

	if not isAuthenticated(request):
		return None

	cloudItemID = parseAjaxParam(ci)
	
	dajax = Dajax()
	cleanPlatform = strip_tags(platform)	
	data = dict()

	try:
		#check that this user has this clouditem
		userCloudItem = CloudItem.objects.filter(id=cloudItemID,reporterID=User.objects.get(id=request.user.id))
		
		if userCloudItem.count() == 1:
			data['tknTable'] = AccessToken.objects.filter(cloudItem=CloudItem.objects.get(id=cloudItemID),serviceType=cleanPlatform)
			data['link'] = cleanPlatform
			data['id'] = cloudItemID
			table = render_to_string("dashboard/tokenTable.html",data)
			dajax.assign(tab, "innerHTML", table)
	except Exception as e:
		dajax.assign(eID, "innetHTML", e)

	return dajax.json()

def submitCode(request, code, ci, platform, eID):
	""" Get the access code from the code """

	if not isAuthenticated(request):
		return None

	cloudItemID = parseAjaxParam(ci)

	dajax = Dajax()
	code = strip_tags(code)

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
	

