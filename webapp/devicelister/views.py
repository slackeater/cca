from django.shortcuts import render, redirect, render_to_response
from django.template import RequestContext
from django.conf import settings
import sys, os, json
from datetime import date
from webapp.func import *
from webapp.exceptionFormatter import formatException
from django.contrib.auth.decorators import login_required
from django import forms
from webapp.exceptionFormatter import formatException
from webapp import constConfig


class DeviceCredentialsForm(forms.Form):
	""" This class represent the form used to log in to the timestamp service """

	uname = forms.EmailField(label="E-Mail",required=True,widget=forms.TextInput(attrs={'class':'form-control'}))
	pwd = forms.CharField(max_length=40,label="Password",required=True,widget=forms.PasswordInput(attrs={'class':'form-control'}))

@login_required
def devicelister(request,cloudItem,tokenID):
	""" Displays the browser file page """

	historyForm = None
	error = None

	try:
		ci = checkCloudItem(cloudItem,request.user.id)
		tkn = checkAccessToken(tokenID,ci)
		credForm = DeviceCredentialsForm()
	except Exception as e:
		error = formatException(e)

	return render_to_response("dashboard/devicelister/devicelisterHome.html", {'tokenID':tkn.id,'objID':ci.id,'showToken':True,'credForm':credForm}, context_instance=RequestContext(request))

