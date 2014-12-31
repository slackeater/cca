from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from cloudservice.forms import MetaSearch
from django.contrib.auth.decorators import login_required
from webapp.func import checkAccessToken, checkCloudItem

@login_required
def mapsView(request,cloudItem,tokenID):
	""" Show the timeline options """

	ci = checkCloudItem(cloudItem,request.user.id)
	at = checkAccessToken(tokenID,ci)
	data = dict()	
	data['objID'] = ci.id
	data['tokenID'] = at.id
	data['showToken'] = True

	return render_to_response("dashboard/maps/mapsHome.html",data,context_instance=RequestContext(request))

