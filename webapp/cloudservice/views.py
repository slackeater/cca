from django.shortcuts import render, render_to_response, redirect
from django.template import RequestContext
from forms import MetaSearch
from dashboard.models import AccessToken
from importer.models import Upload
import md5, base64

# Create your views here.

TEMPLATE = "dashboard/cloudservice/cloudHome.html"

def googleView(request, importID, tokenID):
	return cloudService(request, "google", importID, tokenID)

def dropboxView(request, importID, tokenID):
	""" Show the service """
	return cloudService(request, "dropbox", importID, tokenID)

def cloudService(request, platform, importID, tokenID):
	""" Display the service """

	if not request.user.is_authenticated():
		return redirect("/login/")

	data = dict()

	if not importID > 0 or not tokenID > 0:
		return None

	try:
		sessionName = md5.new(tokenID).hexdigest()
		retrieveCredentials(request, importID, tokenID, sessionName)
		data['objID'] = importID
		data['platform'] = platform
		data['platformTitle'] = platform.title()
		data['updateAnalysis'] = True
		data['tokenID'] = tokenID
		data['resForm'] = MetaSearch()

	except Exception as e:
		data['sessionError'] = e

	return render_to_response(TEMPLATE, data, context_instance=RequestContext(request))

def retrieveCredentials(request, importID, tokenID, sessionName):
	""" Create a session with credentials """

	#check if a session with credentials has been already created
	sessionCred = request.session.get(sessionName, "none") 

	if sessionCred != "none":
		#we already have this variable set
		return None

	# we have all the parameters
	try:
		token = AccessToken.objects.get(importID=Upload.objects.get(id=importID), id=tokenID)
																		
		# create credentials
		request.session[sessionName] = base64.b64decode(token.accessToken)
		return True
	except AccessToken.DoesNotExist:
		raise Exception("Invalid parameters")	
