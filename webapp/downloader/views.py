from django.shortcuts import render, render_to_response, redirect
from django.template import RequestContext
from webapp.func import *
from webapp import constConfig
import oauth
from models import AccessToken,Download
from clouditem.models import CloudItem
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.models import User
from threadmanager import ThreadManager

# Create your views here.


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
			data['metaWait'] = "Not started"
			data['fileWait'] = "Not started"
			data['historyWait'] = "Not started"
			data['objID'] = cloudItem
			data['tokenID'] = t

			#button has been clicked
			if request.method == "POST" and request.POST['start']:
				down = Download.objects.get(tokenID=at)

				if down.threadStatus not in [constConfig.THREAD_DOWN,constConfig.THREAD_INIT,constConfig.THREAD_PHASE_1,constConfig.THREAD_PHASE_2,constConfig.THREAD_PHASE_3,constConfig.THREAD_STOP]:
					#start the download thread
					tm = ThreadManager(t)
					tm.download()
					data['btnClicked'] = True

			#default check to start the periodically ajax function
			try:
				# check to start 
				down = Download.objects.get(tokenID=at)
			except Download.DoesNotExist:
				down = Download(threadStatus=constConfig.THREAD_NOTCLICKED,tokenID=at,folder=sessionName(t))
				down.save()

			if down:
				data['downStatus'] = down.threadStatus

		except Exception as e:
			data['errors'] = e.message
		
		return render_to_response("dashboard/down.html", data, context_instance=RequestContext(request))
	else:
		return redirect("/login/")
