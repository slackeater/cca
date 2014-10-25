from django.shortcuts import render, redirect, render_to_response
from django.template import RequestContext
from django.forms import ModelForm
from django import forms
from models import Upload
from django.http import HttpResponse
from dajaxice.core import dajaxice_functions
from dajaxice.core import dajaxice_config

# Create your views here.

class UploadForm(forms.Form):
	fileUp = forms.FileField(label='File')

def importer(request):
	if request.user.is_authenticated():

		if request.method == "POST":
			form = UploadForm(request.POST, request.FILES)

			if form.is_valid():
				try:
					fileUpload = request.FILES['fileUp']
					with open('/tmp/' + fileUpload.name, 'wb+') as destination:
						for chunk in fileUpload.chunks():
							destination.write(chunk)
					
					status = "Upload of " + fileUpload.name + " was successful."

					# TODO add IP
					newUpload = Upload(fileName=fileUpload.name)
					newUpload.save()
				except Exception as e:
					status = e.message

				# store file name for AJAX	
				request.session['fileName'] = fileUpload.name
				return render_to_response("importer/imp.html", {'form': form, 'upload': status, 'uploadFile': True}, context_instance=RequestContext(request))
		else:
			form = UploadForm()
			return render_to_response("importer/imp.html", {'form': form}, context_instance=RequestContext(request))
	else:
		return redirect("/login/")
