from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register, dajaxice_functions
from django.conf import settings
import sys, os, json, zipfile,sys
from webapp.func import *
from webapp.exceptionFormatter import formatException
from django.template.loader import render_to_string
from clouditem.models import CloudItem
from django.contrib.auth.models import User
from django.utils.dateformat import format
from django.contrib.auth.decorators import login_required
from views import HistoryTimeLineForm,ProfileSelectorForm
from dajaxice.utils import deserialize_form
from webapp.browserfileController import BrowserFileController

@dajaxice_register
@login_required
def fileTimeLine(request,formHistory,profileForm,ci):

	dajax = Dajax()

	try:	
		#check that the import belong to the clouditem
		cloudQuery = checkCloudItem(ci,request.user.id)
		jsonReport = openReport(cloudQuery)

		f = HistoryTimeLineForm(deserialize_form(formHistory))
		
		fProfile = ProfileSelectorForm(deserialize_form(profileForm))
		fProfile.setChoices(jsonReport)

		if f.is_valid() and fProfile.is_valid():
			bc = BrowserFileController(cloudQuery,fProfile.cleaned_data['choices'])
			res = bc.generateTimeLine(f.cleaned_data['domainFilter'])
			
			print type(f.cleaned_data['startDate'])
			print type(f.cleaned_data['endDate'])

			table = render_to_string("clouditem/browserTimeLine.html", {'events':res})
			dajax.assign("#historyShow","innerHTML",table)
			dajax.assign("#historyError","innerHTML","")
			dajax.remove_css_class("#historyError",['alert','alert-danger'])
		else:
			dajax.assign("#historyShow","innerHTML","")
			dajax.assign("#historyError","innerHTML","Invalid Form")
			dajax.add_css_class("#historyError",['alert','alert-danger'])
	except Exception as e:
		dajax.add_css_class("#historyError",['alert','alert-danger'])
		dajax.assign("#historyError","innerHTML",formatException(e))

	return dajax.json()
