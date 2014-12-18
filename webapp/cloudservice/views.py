from django.shortcuts import render, render_to_response, redirect
from django.template import RequestContext
from forms import MetaSearch
from downloader.models import AccessToken
from webapp.func import *

def cloudService(request, cloudItem, tokenID):
	""" Display the service """

	if not isAuthenticated(request):
		return redirect("/login/")

	data = dict()
	ci = checkCloudItem(cloudItem,request.user.id)
	tkn = checkAccessToken(tokenID,ci)


	try:
		#reset search cache
		if "searchCacheID" in request.session:
			request.session.pop("searchCacheID")

		if "searchCache" in request.session:
			request.session.pop("searchCache")


		data['showToken'] = True
		data['objID'] = ci.id

		data['platform'] = tkn.serviceType
		data['platformTitle'] = tkn.serviceType.title()
		data['updateAnalysis'] = True
		data['tokenID'] = tkn.id
		data['resForm'] = MetaSearch()
		data['btnAction'] = "startRes(0)"
	except Exception as e:
		data['sessionError'] = e.message

	return render_to_response("dashboard/cloudservice/cloudHome.html", data, context_instance=RequestContext(request))
