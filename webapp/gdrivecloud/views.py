from django.shortcuts import render, render_to_response, redirect
from django.template import RequestContext
import drive

# Create your views here.

def gdriveViewer(request):
	""" Display the function page """
	if request.user.is_authenticated():

		# set a session with with credentials (session-importID-tokenID)
		data = dict()
		importIDget = int(request.GET.get("i",0))
		tokenID = int(request.GET.get("t",0))
		sessionName = "session" + str(importIDget) + "-" + str(tokenID)

		try:
			drive.retrieveCredentials(request, importIDget, tokenID, sessionName)
			
			#user info
			info = drive.userInformation(request, sessionName, tokenID)
			data.update(info)

		except Exception as e:
			data['sessionError'] = e.message
	
		
		data["objID"] = importIDget
		data["platformTitle"] = "Google"
		data['cloudServiceJavascript'] = "/static/googleFunc.js"
		return render_to_response("cloudservice/cloudHome.html", data, context_instance=RequestContext(request))
	else:
		return redirect("/login/")
