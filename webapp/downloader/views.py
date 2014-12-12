from django.shortcuts import render, render_to_response, redirect
from django.template import RequestContext
from webapp.func import *
from webapp import constConfig
import oauth
from models import AccessToken,Download
from clouditem.models import CloudItem
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.models import User
from django import forms
import json,base64
from tasks import download

# Create your views here.

class TSCredentialsForm(forms.Form):
	uname = forms.CharField(max_length=10,label="Account",required=True)
	pwd = forms.CharField(max_length=20,label="Password",required=True,widget=forms.PasswordInput())

def showTokenDash(request,cloudItem):
	""" Displays the dashboard and manage the menu choices """
	data = {}
	
	if isAuthenticated(request):
		ci = checkCloudItem(cloudItem,request.user.id)
		data['showToken'] = True
		data['objID'] = ci.id
		data['dropAuthURL'] = oauth.dropboxAuthorizeURL()
		data['gdriveAuthURL'] = oauth.googleAuthorizeURL()
		return render_to_response("dashboard/cloud.html", data, context_instance=RequestContext(request))
	else:
		return redirect("/login/")

def showTokenSelect(request,cloudItem,tokenID):
	""" Displays the dashboard and manage the menu choices """
	data = {}
	
	if isAuthenticated(request):
		ci = checkCloudItem(cloudItem,request.user.id)
		tkn = checkAccessToken(tokenID,ci)
		data['showToken'] = True
		data['objID'] = ci.id
		data['tokenID'] = tkn.id
		return render_to_response("dashboard/tknDash.html", data, context_instance=RequestContext(request))
	else:
		return redirect("/login/")

@csrf_protect
def showDownloadDash(request,cloudItem,t):
	""" Displays the dashboard of the download """

	if isAuthenticated(request):
		down = None
		data = {}

		ci = checkCloudItem(cloudItem,request.user.id)
		at = checkAccessToken(t,ci)

		try:
			data['showToken'] = True
			data['credVerified'] = "Not started"
			data['metaWait'] = "Not started"
			data['downSize'] = "Not started"
			data['fileWait'] = "Not started"
			data['verificationWait'] = "Not started"
			data['objID'] = cloudItem
			data['tokenID'] = t
			data['form'] = TSCredentialsForm()

			#button has been clicked
			if request.method == "POST":

				subForm = TSCredentialsForm(request.POST)

				if subForm.is_valid():
					down = Download.objects.get(tokenID=at)
					down.threadStatus = constConfig.THREAD_CLICKED
					down.save()
					pwd = subForm.cleaned_data['pwd']
					account = subForm.cleaned_data['uname']
					download.delay(down,account,pwd)
				else:
					raise Exception("Invalid form")

			#default check to start the periodically ajax function
			try:
				# check to start 
				down = Download.objects.get(tokenID=at)
			except Download.DoesNotExist:
				down = Download(threadStatus=constConfig.THREAD_NOTCLICKED,tokenID=at,folder=sessionName(t))
				down.save()

			if down:
				data['downStatus'] = down.threadStatus
				data['downMessage'] = down.threadMessage

		except Exception as e:
			data['errors'] = e.message
		
		return render_to_response("dashboard/down.html", data, context_instance=RequestContext(request))
	else:
		return redirect("/login/")
