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

class ProfileSelectorForm(forms.Form):
	""" This class represent a Form for choose a browser profile """

	def setChoices(self,report):
		""" Set the choices for the profile of the browser """
		if report is not None:
			browser = report[1]['objects']

			if browser is not None:
				browserChoices = list()
	
				#compute select list
				for b in browser:
					if "chrome" in b['name'].lower():
						formString = constConfig.HISTORY_FORM_CHROME
					elif "firefox" in b['name'].lower():
						formString = constConfig.HISTORY_FORM_FF
					elif "thunderbird" in b['name'].lower():
						formString = constConfig.HISTORY_FORM_TH

					for p in b['profiles']:
						formValue = str(formString)+"_"+p['profileName']	
						browserChoices.append((formValue,b['name']+" - "+p['profileName']))
			
				ch = forms.ChoiceField(label="Profile",widget=forms.Select(attrs={'class':'form-control'}),choices=browserChoices)
				self.fields['choices'] = ch



class HistoryTimeLineForm(forms.Form):
	""" This class represent a Form used to display the history form """

	startDateYear = date.today().year
	
	domainFilter = forms.CharField(label="Domain Filter",required=False,widget=forms.TextInput(attrs={'class':'form-control'}))

	startDate = forms.DateField(initial="31/12/"+str(startDateYear-2),input_formats=['%d/%m/%Y'],widget=forms.DateInput(format='%d/%m/%Y',attrs={'id':'dp1','class':'form-control'}))
	endDate = forms.DateField(initial="31/12/"+str(startDateYear),input_formats=['%d/%m/%Y'],widget=forms.DateInput(format='%d/%m/%Y',attrs={'id':'dp2','class':'form-control'}))

@login_required
def browserfiles(request,cloudItem):
	""" Displays the browser file page """

	browser = None
	historyForm = None
	error = None

	try:
		ci = checkCloudItem(cloudItem,request.user.id)
		report = openReport(ci)
		profileForm = ProfileSelectorForm()
		profileForm.setChoices(report)
		historyForm = HistoryTimeLineForm()
	except Exception as e:
		error = formatException(e)

	return render_to_response("clouditem/browserHome.html", {'browser':browser,'form':historyForm,'profileForm': profileForm,'objID':ci.id,'error':error}, context_instance=RequestContext(request))

