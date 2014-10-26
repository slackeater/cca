from django.shortcuts import render, redirect, render_to_response
from django.template import RequestContext
from django.forms import ModelForm
from django import forms
from models import Upload
from django.http import HttpResponse
from dajaxice.core import dajaxice_functions
from dajaxice.core import dajaxice_config
from django.conf import settings
import os

# Create your views here.

class UploadForm(forms.Form):
	fileUp = forms.FileField(label='File')

def importer(request):
	if request.user.is_authenticated():
		# get all report imported
		rep = Upload.objects.all()

		if request.method == "POST":
			form = UploadForm(request.POST, request.FILES)

			if form.is_valid():
				try:
					fileUpload = request.FILES['fileUp']
					with open(os.path.join(settings.UPLOAD_DIR,fileUpload.name), 'wb+') as destination:
						for chunk in fileUpload.chunks():
							destination.write(chunk)
					
					status = "Upload of " + fileUpload.name + " was successful."

					# TODO add IP
					newUpload = Upload(fileName=fileUpload.name)
					newUpload.save()
					
					# store file name for AJAX	
					request.session['fileName'] = fileUpload.name
					request.session['lastID'] = newUpload.id
				except Exception as e:
					status = e.message

				return render_to_response("importer/imp.html", {'form': form, 'upload': status, 'uploadFile': True, 'repList': rep}, context_instance=RequestContext(request))
		else:
			form = UploadForm()
			return render_to_response("importer/imp.html", {'form': form, 'repList': rep}, context_instance=RequestContext(request))
	else:
		return redirect("/login/")
