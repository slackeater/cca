from django.shortcuts import render, render_to_response, redirect
from django.template import RequestContext
from webapp.func import isAuthenticated
import oauth
from models import AccessToken,Download

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

def showDownloadDash(request,cloudItem,t):
	""" Displays the dashboard of the download """

	if isAuthenticated(request):
		down = None
		data = {}

		try:
			# check to start 
			down = Download.objects.get(tokenID=AccessToken.objects.get(id=t))
		except Download.DoesNotExist:
			down = Download(status=-1,tokenID=AccessToken.objects.get(id=t))
			down.save()

		if down:
			data['downStatus'] = down.status

		data['objID'] = cloudItem
		data['tokenID'] = t

		return render_to_response("dashboard/down.html", data, context_instance=RequestContext(request))
	else:
		return redirect("/login/")
