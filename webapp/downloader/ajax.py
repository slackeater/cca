from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register
from django.core.exceptions import MultipleObjectsReturned
import sys, dropbox
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
from webapp.databaseInterface import DbInterface
from django.contrib.auth.decorators import login_required

@dajaxice_register
@login_required
def checkDownload(request,t,i):
	""" Check the download status """

	dajax = Dajax()

	try:
		tokenID = parseAjaxParam(t)
		cloudItem  = checkCloudItem(i,request.user.id)
		tokenQuery = checkAccessToken(t,cloudItem)

		downloadToken = Download.objects.get(tokenID=tokenQuery)

		#check the status
		s = downloadToken.threadStatus
		dajax.assign("#thStatus","innerHTML",s)	
		dajax.assign("#thMessage","innerHTML",downloadToken.threadMessage)	

		if s != constConfig.THREAD_NOTCLICKED and s != constConfig.THREAD_STOP:
			mask = {constConfig.THREAD_VERIFY_CRED: False, 
				constConfig.THREAD_DOWN_META: False, 
				constConfig.THREAD_COMPUTING: False,
				constConfig.THREAD_DOWN_FH: False,
				constConfig.THREAD_TS: False
				}

			#set the icons that have to use accept.png as icon
			for key,value in mask.iteritems():
				if key <= s:
					mask[key] = True

			#now that states for icon are set, assign to dajax
			for key,value in mask.iteritems():
				if value is True:
					dajax.assign("#status"+str(key),"innerHTML","<img src='/static/icons/accept.png' />")

					if key >= constConfig.THREAD_COMPUTING:
						computeSize = float(downloadToken.downloadSize)/math.pow(2,20)
						dajax.assign("#fileSize","innerHTML",computeSize)
				else: 
					dajax.assign("#status"+str(key),"innerHTML","<img src='/static/loadersmall.gif' />")

		dajax.assign("#errors","innerHTML","")

	except Exception as e:
		dajax.assign("#errors","innerHTML",formatException(e))
	
	return dajax.json()
