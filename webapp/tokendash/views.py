from django.shortcuts import render, render_to_response, redirect
from django.template import RequestContext
from django.template.loader import render_to_string
from webapp.func import *
from webapp import constConfig
import oauth
from downloader.models import AccessToken
from clouditem.models import CloudItem
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.models import User
from django import forms
import json,base64
from django.contrib.auth.decorators import login_required
from webapp.databaseInterface import DbInterface

# Create your views here.

@login_required
def showTokenDash(request,cloudItem):
	""" Displays the dashboard and manage the menu choices """
	data = {}
	
	ci = checkCloudItem(cloudItem,request.user.id)
	data['showToken'] = True
	data['objID'] = ci.id
	data['dropAuthURL'] = oauth.dropboxAuthorizeURL()
	data['gdriveAuthURL'] = oauth.googleAuthorizeURL()

        #for cred
	res = openReport(ci)
	if res is not None:
		data['browsers'] = res[1]["objects"]
	else:
		data['browsers'] = None

        data['accessTable'] = render_to_string("dashboard/tokenTable.html",{'tknTable':DbInterface.getAccessTokenList(ci),'id':ci.id}) 

	return render_to_response("dashboard/cloud.html", data, context_instance=RequestContext(request))

@login_required
def showTokenSelect(request,cloudItem,tokenID):
	""" Displays the dashboard and manage the menu choices """
	data = {}
	
	ci = checkCloudItem(cloudItem,request.user.id)
	tkn = checkAccessToken(tokenID,ci)
	data['showToken'] = True
	data['objID'] = ci.id
	data['tokenID'] = tkn.id
	data['acc'] = json.loads(base64.b64decode(tkn.userInfo))
	return render_to_response("dashboard/tknDash.html", data, context_instance=RequestContext(request))
