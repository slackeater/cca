from django.shortcuts import render, render_to_response, redirect
from django.template import RequestContext
from importer.models import Upload
from django.conf import settings
import json, os

# Create your views here.

def showdash(request):
	""" Displays the dashboard and manage the menu choices """
	data = {}
	tmpl = "dash.html"

	if request.user.is_authenticated():
		if request.method == "GET" and request.GET['i'] is not None:
			c = request.GET.get('c', "null")
			s = request.GET.get('s', 'null')

			if s == "display":
				data = importViewer(request)
				tmpl = "viewer.html"
			elif c == "display":
				cloudDownloader(request)
				tmpl = "cloud.html"

			data['objID'] = request.GET['i']
			return render_to_response("dashboard/" + tmpl, data, context_instance=RequestContext(request))

	else:
		return redirect("/login/")

def importViewer(request):
	""" Manage the view of the reporter """
	uploadID = request.GET['i']
	up = Upload.objects.get(id=uploadID)
	data =  { 'up': up }

	#get report content
	if up.fileName.endswith(".zip.enc"):
		name = up.fileName[:-8]
	else:
		# TODO exception
		return None

	fileName = os.path.join(settings.UPLOAD_DIR, name, name+".report")
	openFile = open(fileName, "r")
	jsonReport = json.load(openFile)

	data['attributes'] = jsonReport[0]['objects']

	browser = jsonReport[1]['objects']
	data['browser'] = jsonReport[1]['objects']
	data['cloud'] = jsonReport[2]['objects']
	
	return data

def cloudDownloader(request):
	""" Download data from the cloud with the credentials found """

