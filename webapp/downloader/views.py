from django.shortcuts import render, render_to_response, redirect
from django.template import RequestContext
from webapp.func import isAuthenticated,sessionName
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
		data['objID'] = cloudItem
		data['dropAuthURL'] = oauth.dropboxAuthorizeURL()
		data['gdriveAuthURL'] = oauth.googleAuthorizeURL()
		return render_to_response("dashboard/cloud.html", data, context_instance=RequestContext(request))
	else:
		return redirect("/login/")

@csrf_protect
def showDownloadDash(request,cloudItem,t):
	""" Displays the dashboard of the download """

	if isAuthenticated(request):
		down = None
		data = {}

		#check if the user has this clouditem
		ci = CloudItem.objects.filter(id=cloudItem,reporterID=User.objects.get(id=request.user.id))

		if ci.count() == 1:
			#check if the token belong to the clouditem
			checkToken = AccessToken.objects.filter(id=t,cloudItem=CloudItem.objects.get(id=cloudItem))

			if checkToken.count() == 1:
	
				at = AccessToken.objects.get(id=t)

				#button has been clicked
				if request.method == "POST" and request.POST['start']:
					down = Download.objects.get(tokenID=at)
					if down.status == -1:
						#start the download thread
						tm = ThreadManager(t)
						tm.download()
				
				#default check to start the periodically ajax function
				try:
					# check to start 
					down = Download.objects.get(tokenID=at)
				except Download.DoesNotExist:
					down = Download(status=-1,tokenID=at,folder=sessionName(t))
					down.save()

				if down:
					data['downStatus'] = down.status

				data['objID'] = cloudItem
				data['tokenID'] = t

		return render_to_response("dashboard/down.html", data, context_instance=RequestContext(request))
	else:
		return redirect("/login/")
