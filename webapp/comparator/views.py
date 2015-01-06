from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from cloudservice.forms import MetaSearch
from webapp.func import isAuthenticated
from forms import VerifyForm
from django.contrib.auth.decorators import login_required

@login_required
def comparatorView(request,cloudItem,tokenID):
	""" Show the timeline options """
	
	#when the page loads display the comparator
	data = dict()	
	data['objID'] = cloudItem
	data['tokenID'] = tokenID
	data['showToken'] = True
	data['form'] = VerifyForm()

	return render_to_response("dashboard/comparator/comparatorHome.html",data,context_instance=RequestContext(request))

