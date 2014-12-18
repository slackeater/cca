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


class HistoryTimeLineForm(forms.Form):

	def __init__(self,choices, *args,**kwargs):
		super(forms.Form,self).__init__(*args,**kwargs)

		self.fields['choices'] = choices

	startDateYear = date.today().year
	
	domainFilter = forms.CharField(label="Domain Filter",widget=forms.TextInput(attrs={'class':'form-control'}))

	startDate = forms.DateField(initial="31/12/"+str(startDateYear-2),required=True,input_formats=['%d/%m/%Y'],widget=forms.DateInput(format='%d/%m/%Y',attrs={'id':'dp1','class':'form-control'}))
	endDate = forms.DateField(initial="31/12/"+str(startDateYear),required=True,input_formats=['%d/%m/%Y'],widget=forms.DateInput(format='%d/%m/%Y',attrs={'id':'dp2','class':'form-control'}))



@login_required
def browserfiles(request,cloudItem):
	
	ci = checkCloudItem(cloudItem,request.user.id)
	
	report = openReport(ci)
	browser = None
	historyForm = None
	error = None
	
	try:
		if report is not None:
			browser = report[1]['objects']

			if browser is not None:
				browserChoices = list()
				i = 0
				#compute select list
				for b in browser:
					for p in b['profiles']:
						browserChoices.append((i,b['name']+" - "+p['profileName']))
					i = i+1

				#this field can be dinamyc so we build it here
				ch = forms.ChoiceField(widget=forms.Select(attrs={'class':'form-control'}),choices=browserChoices)

				historyForm = HistoryTimeLineForm(ch)
		else:
			error = "No report found for this cloud item"
	except Exception as e:
		error = formatException(e)
		

	return render_to_response("clouditem/browserHome.html", {'browser':browser,'form':historyForm,'objID':ci.id,'error':error}, context_instance=RequestContext(request))


