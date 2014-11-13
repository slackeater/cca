from django.shortcuts import render, redirect, render_to_response
from importer.models import Upload 
from models import CloudItem
from django.template import RequestContext
from django.utils import timezone
from webapp.func import isAuthenticated
from forms import CloudItemForm
from django.utils.html import strip_tags
from django.contrib.auth.models import User
# Create your views here.


def cloudItem(request):

	if isAuthenticated(request):
		f = CloudItemForm()
		
		if request.POST:
			f = CloudItemForm(request.POST)

			if f.is_valid():
				c = CloudItem(desc=f.cleaned_data['description'],reportName=f.cleaned_data['name'],reporterID=User.objects.get(id=request.user.id))
				c.save()

		clouds = CloudItem.objects.filter(reporterID=User.objects.get(id=request.user.id))
		data = {'cloudItem': clouds,'form':f}
		return render_to_response("clouditem/clouditemHome.html", data, context_instance=RequestContext(request))
	else:
		return redirect("/login/")


def showCloudItem(request,itemID):
	""" Display a cloud item """

	if isAuthenticated(request):
		getItem = CloudItem.objects.filter(id=itemID,reporterID=User.objects.get(id=request.user.id))
		data = {'item': getItem,'objID': itemID}
		return render_to_response("dashboard/dash.html", data, context_instance=RequestContext(request))
	else:
		return redirect("/login/")
