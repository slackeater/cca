from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from cloudservice.forms import MetaSearch
from webapp.func import *

# Create your views here.

def showTimeline(request,cloudItem,tokenID):
	""" Show the timeline options """

	if isAuthenticated(request):

		ci = checkCloudItem(cloudItem,request.user.id)
		tkn = checkAccessToken(tokenID,ci)

		data = dict()	
		data['objID'] = ci.id
		data['tokenID'] = tkn.id
		data['resForm'] = MetaSearch()
		data['showToken'] = True
		data['btnAction'] = "formTimeline()"

		return render_to_response("dashboard/timeliner/timeHome.html",data,context_instance=RequestContext(request))
	else:
		return redirect("/login/")

