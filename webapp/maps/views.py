from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from cloudservice.forms import MetaSearch
from webapp.func import isAuthenticated

# Create your views here.

def mapsView(request,cloudItem,tokenID):
	""" Show the timeline options """

	if isAuthenticated(request):
		data = dict()	
		data['objID'] = cloudItem
		data['tokenID'] = tokenID
		data['showToken'] = True

		return render_to_response("dashboard/maps/mapsHome.html",data,context_instance=RequestContext(request))
	else:
		return redirect("/login/")

