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

# Create your views here.

class UploadForm(forms.Form):
	fileUp = forms.FileField(label='File')

def importer(request,cloudItem):
	if request.user.is_authenticated():
		# get all report imported
		rep = Upload.objects.all()
		status = ""

		if request.method == "POST":
			
			form = UploadForm(request.POST, request.FILES)

			if form.is_valid():
				try:
					manageReportUpload(request,cloudItem)
				except Exception as e:
					status = e.message

				return render_to_response("dashboard/imp.html", {'objID': cloudItem,'form': form, 'upload': status, 'repList': rep}, context_instance=RequestContext(request))
		else:
			
			form = UploadForm()
			return render_to_response("dashboard/imp.html", {'objID': cloudItem,'form': form, 'repList': rep}, context_instance=RequestContext(request))
	else:
		return redirect("/login/")


def manageReportUpload(request,cloudItem):
	""" Uncrypt and store the report """

	# add path for crypto
	cryptoPath = os.path.join(os.path.dirname(settings.BASE_DIR), "finder")

	if not cryptoPath in sys.path:
			sys.path.insert(1, cryptoPath)
			del cryptoPath

	import crypto

	fileUpload = request.FILES['fileUp']

	#write to disk
	with open(os.path.join(settings.UPLOAD_DIR,fileUpload.name), 'wb+') as destination:
		for chunk in fileUpload.chunks():
			destination.write(chunk)
	
	fileCont = open(os.path.join(settings.UPLOAD_DIR,fileUpload.name), "r")
	jsonParsed = json.load(fileCont)

	cont = jsonParsed['enc']
	k = jsonParsed['k']

	#decrypt AES key
	aes = crypto.decryptRSA(k)

	#decrypt ZIP - first write encrypted cont into a temp file, read it, decrypt it and store the ZIP
	tempFileName = os.path.join(settings.UPLOAD_DIR, fileUpload.name+".tmp")
	open(tempFileName, "w+b").write(cont)

	# fernet wants "bytes" as token
	fileBytes = crypto.decryptFernetFile(open(tempFileName, "rb").read(), aes)
	print fileUpload.name[-4:]

	if fileUpload.name.endswith(".enc"):
		name = fileUpload.name[:-4] 
	else:
		raise Exception("Invalid filename.")

	#write decrypted file to disc
	decZipFile = os.path.join(settings.UPLOAD_DIR, name)
	open(decZipFile, "w+b").write(fileBytes)

	#delete temp file
	os.remove(tempFileName)

	aes = None
	del aes
	
	#unzip
	fileZip = zipfile.ZipFile(decZipFile)
	fileZip.extractall(settings.UPLOAD_DIR)

	# set this report parsed	
	newUpload = Upload(fileName=fileUpload.name,uploadIP=request.META['REMOTE_ADDR'],parsed=True)
	newUpload.save()

	#add foreign key to cloud item
	cItem = CloudItem.objects.get(id=cloudItem)
	cItem.importID = newUpload
	cItem.save()
