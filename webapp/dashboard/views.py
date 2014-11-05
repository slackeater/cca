from django.shortcuts import render, render_to_response, redirect
from django.template import RequestContext
from django.template.loader import render_to_string
from importer.models import Upload
from models import DropboxToken, GoogleDriveToken
from django.conf import settings
import dropbox, base64
import json, os, oauth

# Create your views here.

def showdash(request):
	""" Displays the dashboard and manage the menu choices """
	data = {}
	
	if request.user.is_authenticated():
		index = request.GET.get('i', 'null')

		if index != 'null':
			s = request.GET.get('s', 'null')

			if s == "display":
				data = importViewer(request)
				tmpl = "viewer.html"
			
			elif s == "cloud":
				data = cloudDownloader(request)
				tmpl = "cloud.html"
					
			return render_to_response("dashboard/" + tmpl, data, context_instance=RequestContext(request))
		else: 
			return redirect("/import/")
	else:
		return redirect("/login/")

def importViewer(request):
	""" Manage the view of the reporter """
	uploadID = request.GET['i']
	up = Upload.objects.get(id=uploadID)
	data =  { 'up': up }

	jsonReport = getReportJson(up)
	data['attributes'] = jsonReport[0]['objects']
	data['browser'] = jsonReport[1]['objects']
	data['cloud'] = jsonReport[2]['objects']
	data['objID'] = uploadID
	
	return data

def cloudDownloader(request):
	""" Download data from the cloud with the credentials found """

	#get all credentials
	importID = request.GET['i']
	up = Upload.objects.get(id=importID)
	jsonReport = getReportJson(up)

	#to show the credentials
	browser = jsonReport[1]['objects']
	data = dict()
	data['dropAuthurl'] = oauth.dropboxAuthorizeURL()
	data["gdriveAuthurl"] = oauth.googleAuthorizeURL()

	
	data["dTab"] = render_to_string("dashboard/tokenTable.html",{"tknTable": DropboxToken.objects.all(),"link": "dropcloud", "id": importID})	
	data["gTab"] = render_to_string("dashboard/tokenTable.html",{"tknTable": GoogleDriveToken.objects.all(), "link": "gdrivecloud", "id": importID})	

	data["browsers"] = browser
	data['objID'] = importID

	return data

def getReportJson(uploadObject):
	""" Read the JSON of the report """

	#get report content
	if uploadObject.fileName.endswith(".zip.enc"):
		name = uploadObject.fileName[:-8]
	else:
		# TODO exception
		return None

	fileName = os.path.join(settings.UPLOAD_DIR, name, name+".report")
	openFile = open(fileName, "r")
	return json.load(openFile)

