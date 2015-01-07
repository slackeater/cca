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
from dajaxice.utils import deserialize_form
from webapp.deviceListController import DeviceListController

@dajaxice_register
@login_required
def listdevices(request,clouditem,tokenID,form):
	""" Call the timeline generator """

	dajax = Dajax()
	print "ciao"
	try:	
		cloudQuery = checkCloudItem(clouditem,request.user.id)
		tkn = checkAccessToken(tokenID,cloudQuery)
	
		dc = DeviceListController(tkn,None,None)
		dc.listDevices()

		print "test"
	except Exception as e:
		print formatException(e)

	return dajax.json()
