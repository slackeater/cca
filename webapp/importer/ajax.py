from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register, dajaxice_functions
from django.conf import settings
import sys, os, json, zipfile
from models import Upload
from webapp.func import *
from django.template.loader import render_to_string
from clouditem.models import CloudItem
from django.contrib.auth.models import User

@dajaxice_register
def showReport(request,up,ci):

	if not isAuthenticated(request):
		return None

	dajax = Dajax()

	#check that the import belong to the clouditem
	uploadID = parseAjaxParam(up)
	cloudQuery = checkCloudItem(ci,request.user.id)

	try:	
		# get the upload
		uploadQuery = Upload.objects.get(cloudItemID=cloudQuery,id=uploadID)
		
		#parse with JSON
		report = os.path.join(settings.UPLOAD_DIR,uploadQuery.fileName,uploadQuery.fileName+".report")
		openReport = open(report,"rb")
		jsonReport = json.load(openReport)

		data = {'attributes': jsonReport[0]['objects'],'browser':jsonReport[1]['objects'],'cloud':jsonReport[2]['objects']}
		
		table = render_to_string("dashboard/impReportView.html", data)
		dajax.assign("#reportTable","innerHTML",table)
	except Exception as e:
		dajax.assign("#repStatus","innerHTML",e)

	return dajax.json()
