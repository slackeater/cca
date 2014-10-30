from django.shortcuts import render, render_to_response, redirect
from django.template import RequestContext
from importer.models import Upload
from models import DropboxToken, DropboxAccountInfo, MimeType
from django.conf import settings
import dropbox, base64
import json, os, drop

# Create your views here.

def showdash(request):
	""" Displays the dashboard and manage the menu choices """
	data = {}
	tmpl = "dash.html"

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
			elif c == "token":
				tknID = request.GET.get('t', "null")

				if tknID != "null":
					data = dropboxCall(tknID)
					tmpl = "drop.html"
					
					#mime types
					mime = MimeType.objects.all()
					data['mimes'] = mime

			data['objID'] = index
			return render_to_response("dashboard/" + tmpl, data, context_instance=RequestContext(request))

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

def dropboxCall(tokenID):
	""" Perform different API calls for dropbox """

	d = {}

	try:
		tkn = DropboxToken.objects.get(id=tokenID)

		try:
			acc = DropboxAccountInfo.objects.get(tokenID=tkn)
			d['account_info'] = json.loads(base64.b64decode(acc.accountInfo))
		except DropboxAccountInfo.DoesNotExist:
			c = dropbox.client.DropboxClient(tkn.accessToken)
			d['account_info'] = c.account_info()
			# store the retrieved object
			acc = DropboxAccountInfo(tokenID=tkn, accountInfo=base64.b64encode(json.dumps(d['account_info'])))
			acc.save()
	except DropboxToken.DoesNotExist:
		None

	return d

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

