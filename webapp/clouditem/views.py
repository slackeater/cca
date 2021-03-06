from django.shortcuts import render, redirect, render_to_response
from importer.models import Upload 
from models import CloudItem
from importer.models import Upload
from django.template import RequestContext
from django.utils import timezone
from webapp.func import isAuthenticated
from django.utils.html import strip_tags
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.decorators import login_required

class CloudItemForm(forms.Form):
	""" A cloud item form """

	name = forms.CharField(max_length=15,label="Name",widget=forms.TextInput(attrs={'class':'form-control'}))
	description = forms.CharField(label="Description",widget=forms.Textarea(attrs={'class':'form-control'}))

@login_required
def cloudItem(request):
	""" View used to show the list of cloud item and add a new one """

	errors = ""
	f = CloudItemForm()
	
	if request.POST:
		f = CloudItemForm(request.POST)

		if f.is_valid():
			c = CloudItem(desc=f.cleaned_data['description'],reportName=f.cleaned_data['name'],reporterID=User.objects.get(id=request.user.id))
			c.save()
		else:
			errors = "Invalid insertion. Please check your data."

	clouds = CloudItem.objects.filter(reporterID=User.objects.get(id=request.user.id))
	res = list()	
	for c in clouds:
		hasReport = False
		reportNumber = Upload.objects.filter(cloudItemID=c)

		if len(reportNumber) == 1:
			hasReport = True

		res.append({'item': c, 'hasReport': hasReport})
			
	data = {'cloudItem': res,'form':f,'errors': errors}
	return render_to_response("clouditem/clouditemHome.html", data, context_instance=RequestContext(request))

@login_required
def showCloudItem(request,itemID):
	""" Display a cloud item """

	getItem = CloudItem.objects.get(id=itemID,reporterID=User.objects.get(id=request.user.id))
	data = {'item': getItem,'objID': itemID}
	return render_to_response("dashboard/dash.html", data, context_instance=RequestContext(request))
