from django.shortcuts import render, render_to_response, redirect
from django.template import RequestContext
from forms import MetaSearch
from downloader.models import AccessToken
import md5, base64
from webapp.func import isAuthenticated

# Create your views here.

def cloudService(request, cloudItem, tokenID):
	""" Display the service """

	if not isAuthenticated(request):
		return redirect("/login/")

	data = dict()

	try:
		data['showToken'] = True
		data['objID'] = cloudItem

		#get platform
		platform = AccessToken.objects.get(id=tokenID)

		data['platform'] = platform.serviceType
		data['platformTitle'] = platform.serviceType.title()
		data['updateAnalysis'] = True
		data['tokenID'] = tokenID
		data['resForm'] = MetaSearch()

	except Exception as e:
		data['sessionError'] = e

	return render_to_response("dashboard/cloudservice/cloudHome.html", data, context_instance=RequestContext(request))
