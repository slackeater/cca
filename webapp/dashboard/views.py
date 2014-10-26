from django.shortcuts import render, render_to_response
from django.template import RequestContext
from importer.models import Upload
from django.conf import settings
import json, os

# Create your views here.

def showdash(request):

	if request.method == "GET":
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

	return render_to_response("dashboard/dash.html", data, context_instance=RequestContext(request))
