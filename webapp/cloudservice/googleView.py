from django.shortcuts import render, render_to_response, redirect
from django.template import RequestContext
import drive
from dropcloud.forms import DropMetaSearch

# Create your views here.

def gdriveViewer(request):
	""" Display the function page """
	if request.user.is_authenticated():

		# set a session with with credentials (sessionimportID-tokenID)
		data = dict()
		importIDget = int(request.GET.get("i",0))
		tokenID = int(request.GET.get("t",0))
		sessionName = "session" + str(importIDget) + "-" + str(tokenID)

		if not tokenID > 0 or not importIDget > 0:
			return None

		try:
			drive.retrieveCredentials(request, importIDget, tokenID, sessionName)
			
			#user info
			info = drive.userInformation(request, sessionName, tokenID)
			data.update(info)
			data["objID"] = importIDget
			data["platformTitle"] = "Google"
			data['cloudServiceJavascript'] = "/static/googleFunc.js"
			data['updateAnalysis'] = True
			data['resForm'] = DropMetaSearch()
		except Exception as e:
			data['sessionError'] = e.message
	
		return render_to_response("cloudservice/cloudHome.html", data, context_instance=RequestContext(request))
	else:
		return redirect("/login/")
