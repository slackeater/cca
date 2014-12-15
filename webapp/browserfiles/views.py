from django.shortcuts import render, redirect, render_to_response
from django.template import RequestContext
from django.conf import settings
import sys, os, json
from datetime import date
from webapp.func import *
from webapp.exceptionFormatter import formatException
from django.contrib.auth.decorators import login_required
from django import forms


class HistoryTimeLineForm(forms.Form):

	def __init__(self,choices,*args, **kwargs):
		super(HistoryTimeLineForm, self).__init__(*args, **kwargs)
		self.fields['captcha'] = choices

	browser = forms.ChoiceField(label="Browser",widget=forms.Select(attrs={'class':'form-control'}))

	startDateYear = date.today().year

	startDate = forms.DateField(initial="31/12/"+str(startDateYear-2),required=True,label="Start Date",input_formats=['%d/%m/%Y'],widget=forms.DateInput(format='%d/%m/%Y',attrs={'id':'dp1','class':'form-control'}))
	endDate = forms.DateField(initial="31/12/"+str(startDateYear),required=True,label="End Date",input_formats=['%d/%m/%Y'],widget=forms.DateInput(format='%d/%m/%Y',attrs={'id':'dp2','class':'form-control'}))



@login_required
def browserfiles(request,cloudItem):

	ci = checkCloudItem(cloudItem,request.user.id)
	browser = openReport(ci)[1]['objects']

	selectChoice = list()
	#compute select list
	for b in browser:
		selectChoice.append((1,b['name']))

	historyForm = HistoryTimeLineForm(selectChoice)
		

	return render_to_response("clouditem/browserHome.html", {'browser':browser,'form':historyForm}, context_instance=RequestContext(request))


