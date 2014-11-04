from django.shortcuts import render, render_to_response, redirect
from django.template import RequestContext
from importer.models import Upload
from models import DropboxAccountInfo
from dashboard.models import DropboxToken
from django.conf import settings
import dropbox, base64
import json, os
from forms import DropMetaSearch

# Create your views here.

def dropViewer(request):
	""" Display the function page """
	if request.user.is_authenticated():
		data = {}
		tknID = request.GET.get("t","null")
		index = request.GET.get("i", "null")
		if tknID != "null" and tknID > 0 and index != "null" and index >= 0:
			data['accountInfo'] = dropboxCall(request,tknID)
			data['resForm'] = DropMetaSearch()
			data['objID'] = index
			return render_to_response("dropcloud/drop.html", data, context_instance=RequestContext(request))
	else:
		return redirect("/login/")


def dropboxCall(request,tokenID):
	""" Perform different API calls for dropbox """

	try:
		tkn = DropboxToken.objects.get(id=tokenID)

		try:
			acc = DropboxAccountInfo.objects.get(tokenID=tkn)
			return json.loads(base64.b64decode(acc.accountInfo))
		except DropboxAccountInfo.DoesNotExist:
			c = dropbox.client.DropboxClient(tkn.accessToken)
			a = c.account_info()
			# store the retrieved object
			acc = DropboxAccountInfo(tokenID=tkn, accountInfo=base64.b64encode(json.dumps(a)))
			acc.save()
			return a
	except DropboxToken.DoesNotExist:
		return None

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

