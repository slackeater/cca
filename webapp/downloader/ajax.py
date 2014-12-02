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
from webapp.func import isAuthenticated,parseAjaxParam
from clouditem.models import CloudItem
from django.contrib.auth.models import User
from webapp import constConfig

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
def checkDownload(request,t):

	if not isAuthenticated(request):
		return None

	tokenID = parseAjaxParam(t)

	dajax = Dajax()

	try:
		tokenQuery = AccessToken.objects.get(id=tokenID)
		cloudItem  = CloudItem.objects.get(id=tokenQuery.cloudItem.id)

		# if the cloud item reporter corresponds to the user
		if cloudItem.reporterID == User.objects.get(id=request.user.id):

			downloadToken = Download.objects.get(tokenID=AccessToken.objects.get(id=tokenID))

			#check the status
			dajax.assign("#thStatus","innerHTML",downloadToken.threadStatus)	
			dajax.assign("#thMessage","innerHTML",downloadToken.threadMessage)	
			dajax.assign("#metaStatus","innerHTML","<img src='/static/loadersmall.gif' />")
			dajax.assign("#fileStatus","innerHTML","<img src='/static/loadersmall.gif' />")
			dajax.assign("#historyStatus","innerHTML","<img src='/static/loadersmall.gif' />")

			if downloadToken.threadStatus == constConfig.THREAD_PHASE_1:
				dajax.assign("#metaStatus","innerHTML","<img src='/static/icons/accept.png' />")
				dajax.assign("#fileStatus","innerHTML","<img src='/static/loadersmall.gif' />")
				dajax.assign("#historyStatus","innerHTML","<img src='/static/loadersmall.gif' />")
			elif downloadToken.threadStatus == constConfig.THREAD_PHASE_2:
				dajax.assign("#metaStatus","innerHTML","<img src='/static/icons/accept.png' />")
				dajax.assign("#fileStatus","innerHTML","<img src='/static/icons/accept.png' />")
				dajax.assign("#historyStatus","innerHTML","<img src='/static/loadersmall.gif' />")
			elif downloadToken.threadStatus == constConfig.THREAD_PHASE_3:
				dajax.assign("#metaStatus","innerHTML","<img src='/static/icons/accept.png' />")
				dajax.assign("#fileStatus","innerHTML","<img src='/static/icons/accept.png' />")
				dajax.assign("#historyStatus","innerHTML","<img src='/static/icons/accept.png' />")
				dajax.assign("#thMessage","innerHTML","Completed.")

	except Exception as e:
		dajax.assign("#errors","innerHTML",e.message)
	
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
	

