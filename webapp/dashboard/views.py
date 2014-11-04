from django.shortcuts import render, render_to_response, redirect
from django.template import RequestContext
from importer.models import Upload
from models import DropboxToken
from django.conf import settings
import dropbox, base64
import json, os, drop

# Create your views here.

def showdash(request):
	""" Displays the dashboard and manage the menu choices """
	data = {}

	if request.user.is_authenticated():
		index = request.GET.get('i', 'null')

		if index != 'null':
			c = request.GET.get('c', "null")
			s = request.GET.get('s', 'null')

			if s == "display":
				data = importViewer(request)
				tmpl = "viewer.html"
			
			elif c == "display":
				data = cloudDownloader(request)
				tmpl = "cloud.html"
					
			data['objID'] = index
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
	
	return data

def cloudDownloader(request):
	""" Download data from the cloud with the credentials found """

	#get all credentials
	importID = request.GET['i']
	up = Upload.objects.get(id=importID)
	jsonReport = getReportJson(up)
	browser = jsonReport[1]['objects']

	data = { 'authurl' : drop.authorizeURL()}

	#get all tokens
	token = DropboxToken.objects.filter(importID=Upload.objects.get(id=importID))
	data["tokens"] = token
	data["browsers"] = browser

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

