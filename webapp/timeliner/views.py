from django.shortcuts import render_to_response
from django.template import RequestContext
from cloudservice.forms import MetaSearch

# Create your views here.

def showTimeline(request,cloudItem,tokenID):
	""" Show the timeline options """
	data = dict()	
	data['objID'] = cloudItem
	data['tokenID'] = tokenID
	data['form'] = MetaSearch()
	data['showToken'] = True

	return render_to_response("dashboard/timeliner/timeHome.html",data,context_instance=RequestContext(request))
