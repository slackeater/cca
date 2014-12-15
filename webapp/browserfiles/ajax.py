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

@dajaxice_register
@login_required
def fileTimeLine(request,up,ci):

	dajax = Dajax()

	try:	
		#check that the import belong to the clouditem
		cloudQuery = checkCloudItem(ci,request.user.id)
		jsonReport = openReport(cloudQuery)[1]["objects"]
			
		table = render_to_string("cloudItem/browserTimeLine.html", {})
		dajax.assign("#reportTable","innerHTML",table)
		dajax.assign("#repStatus","innerHTML","")
	except Exception as e:
		dajax.assign("#repStatus","innerHTML",formatException(e))

	return dajax.json()
