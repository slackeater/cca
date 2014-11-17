from django.shortcuts import render_to_response
from django.template import RequestContext

# Create your views here.

def showTimeline(request,cloudItem,tokenID):
	""" Show the timeline options """
	data = dict()	
	data['objID'] = cloudItem
	data['tokenID'] = tokenID

	return render_to_response("dashboard/timeliner/timeHome.html",data,context_instance=RequestContext(request))
