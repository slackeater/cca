from django.shortcuts import render, redirect, render_to_response
from django.template import RequestContext
from django.forms import ModelForm
from django import forms
from models import Upload
from django.http import HttpResponse
from clouditem.models import CloudItem
from dajaxice.core import dajaxice_functions
from dajaxice.core import dajaxice_config
from django.conf import settings
import sys, os, json, zipfile
from django.utils.html import strip_tags
from django.contrib.auth.models import User
from webapp.func import *
from webapp.exceptionFormatter import formatException
from django.utils import timezone
from django.utils.dateformat import format

class UploadForm(forms.Form):
	fileUp = forms.FileField(label='File')

def importer(request,cloudItem):

	if isAuthenticated(request):
	
		form = None
		status = None
		rep = None
		cloudItemQuery = CloudItem.objects.get(reporterID=User.objects.get(id=request.user.id),id=cloudItem)

		try:
			if request.method == "POST":
				form = UploadForm(request.POST, request.FILES)

				if form.is_valid():
					manageReportUpload(request,cloudItem)
		
			# get all report imported for this clouditem

			rep = Upload.objects.filter(cloudItemID=cloudItemQuery)
			form = UploadForm() if rep.count() == 0 else None 
		except Exception as e:
			status = formatException(e)

		return render_to_response("dashboard/imp.html", {'parseStatus': status,'objID': cloudItem,'form': form, 'repList': rep}, context_instance=RequestContext(request))
	else:
		return redirect("/login/")


def manageReportUpload(request,cloudItem):
	""" Uncrypt and store the report """
	
	#check if an item is already in the DB
	impDb = Upload.objects.filter(cloudItemID=CloudItem.objects.get(id=cloudItem))
	
	if len(impDb) != 0:
		raise ("A report already exists.")

	# add path for crypto
	cryptoPath = os.path.join(os.path.dirname(settings.BASE_DIR), "finder")

	if not cryptoPath in sys.path:
			sys.path.insert(1, cryptoPath)
			del cryptoPath

	import crypto

	fileUpload = request.FILES['fileUp']
	fileName = strip_tags(fileUpload.name)
	#create a folder for this cloud item if do not exists
	path = os.path.join(settings.UPLOAD_DIR,cloudItem)

	if not os.path.isdir(path):
		os.mkdir(path)

	#upload name
	upTime = timezone.now()
	shaName = fileName
	uploadName = crypto.sha256(shaName[:-8]+crypto.HASH_SEPARATOR+format(upTime,"U")).hexdigest()
	
	wholeUploadPath = os.path.join(path,uploadName)

	if not os.path.isdir(wholeUploadPath):
		os.mkdir(wholeUploadPath)

	#write to disk
	with open(os.path.join(wholeUploadPath,fileName), 'wb+') as destination:
		for chunk in fileUpload.chunks():
			destination.write(chunk)
	
	fileCont = open(os.path.join(wholeUploadPath,fileName), "r")
	jsonParsed = json.load(fileCont)

	cont = jsonParsed['enc']
	k = jsonParsed['k']

	#decrypt AES key
	aes = crypto.decryptRSA(k)

	#decrypt ZIP - first write encrypted cont into a temp file, read it, decrypt it and store the ZIP
	tempFileName = os.path.join(wholeUploadPath,fileName+".tmp")
	open(tempFileName, "w+b").write(cont)

	# fernet wants "bytes" as token
	fileBytes = crypto.decryptFernetFile(open(tempFileName, "rb").read(), aes)

	if fileName.endswith(".enc"):
		name = fileName[:-4] 
	else:
		raise Exception("Invalid filename.")

	#write decrypted file to disc
	decZipFile = os.path.join(wholeUploadPath, name)
	open(decZipFile, "w+b").write(fileBytes)

	#delete temp file
	os.remove(tempFileName)

	aes = None
	del aes
	
	#unzip
	fileZip = zipfile.ZipFile(decZipFile)
	fileZip.extractall(wholeUploadPath)
	# set this report parsed	
	newUpload = Upload(fileName=name[:-4],uploadDate=upTime,uploadIP=request.META['REMOTE_ADDR'],parsed=True,cloudItemID=CloudItem.objects.get(id=cloudItem))
	newUpload.save()
