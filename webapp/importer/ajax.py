from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register, dajaxice_functions
from django.conf import settings
import sys, os, json, zipfile,sys
from models import Upload
from webapp.func import *
from webapp.exceptionFormatter import formatException
from django.template.loader import render_to_string
from clouditem.models import CloudItem
from django.contrib.auth.models import User
from django.utils.dateformat import format


# add path for crypto
cryptoPath = os.path.join(os.path.dirname(settings.BASE_DIR), "finder")

if not cryptoPath in sys.path:
	sys.path.insert(1, cryptoPath)
	del cryptoPath

import crypto

@dajaxice_register
def showReport(request,up,ci):

	if not isAuthenticated(request):
		return None

	dajax = Dajax()

	try:	
		#check that the import belong to the clouditem
		uploadID = parseAjaxParam(up)
		cloudQuery = checkCloudItem(ci,request.user.id)

		# get the upload
		uploadQuery = Upload.objects.get(cloudItemID=cloudQuery,id=uploadID)

		#build the name of the folder
		hashFolder = str(crypto.sha256(uploadQuery.fileName+crypto.HASH_SEPARATOR+format(uploadQuery.uploadDate,"U")).hexdigest())
		
		#parse with JSON
		report = os.path.join(settings.UPLOAD_DIR,str(cloudQuery.id),hashFolder,uploadQuery.fileName,uploadQuery.fileName+".report")
		
		openReport = open(report,"rb")
		jsonReport = json.load(openReport)

		data = {'attributes': jsonReport[0]['objects'],'browser':jsonReport[1]['objects'],'cloud':jsonReport[2]['objects']}
		
		table = render_to_string("dashboard/impReportView.html", data)
		dajax.assign("#reportTable","innerHTML",table)
		dajax.assign("#repStatus","innerHTML","")
	except Exception as e:
		dajax.assign("#repStatus","innerHTML",formatException(e))

	return dajax.json()
