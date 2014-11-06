from django.shortcuts import render, render_to_response, redirect
from django.template import RequestContext
from models import GoogleAccountInfo
from dashboard.models import GoogleDriveToken
import drive
import base64, json

# Create your views here.

def gdriveViewer(request):
	""" Display the function page """
	if request.user.is_authenticated():

		# set a session with with credentials (session-importID-tokenID)
		data = dict()
		importIDget = int(request.GET.get("i",0))
		tokenID = int(request.GET.get("t",0))
		sessionName = "session" + str(importIDget) + "-" + str(tokenID)

		#try:
		drive.retrieveCredentials(request, importIDget, tokenID, sessionName)
		uInfo = userInformation(request, sessionName, tokenID)
		data = uInfo
		#except Exception as e:
		#	print e
		#	data['sessionError'] = e.message
		
		data["objID"] = importIDget
		return render_to_response("gdrivecloud/gdrive.html", data, context_instance=RequestContext(request))


	else:
		return redirect("/login/")

def userInformation(request,sessionName, tokenID):
	""" Print the user account information """ 
	userInfo = dict()
	#insert into database if not present
	obj, created = GoogleAccountInfo.objects.get_or_create(tokenID=GoogleDriveToken(id=tokenID))

	if created == True:
		httpObj = drive.httpCreator(sessionName,request.session[sessionName])
		user_info_service = drive.serviceBuilder("oauth2","v2",httpObj)
		info = user_info_service.userinfo().get().execute()
		
		#update the object
		userInfo['info'] = info
		obj.accountInfo = base64.b64encode(json.dumps(info))
		obj.save()
	# userinfo already present
	elif created == False:
		userInfo['info'] = json.loads(base64.b64decode(obj.accountInfo))

	return userInfo


	
