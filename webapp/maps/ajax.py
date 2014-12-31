from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register
from dajaxice.utils import deserialize_form
from webapp.func import *
from webapp.exceptionFormatter import formatException
from downloader.models import FileDownload, Download
from django.template.loader import render_to_string
from django.utils.html import strip_tags,strip_entities
import time,sys,traceback
from webapp.mapsController import MapsController
from django.contrib.auth.decorators import login_required

@dajaxice_register
@login_required
def exifMap(request,cloudItem,tokenID):
	
	dajax = Dajax()

	try:
		t = parseAjaxParam(tokenID)
		ci = checkCloudItem(cloudItem,request.user.id)
		tkn = checkAccessToken(t,ci)
	
		mc = MapsController(tkn)
		r = mc.findExif()
		
		table = render_to_string("dashboard/maps/exifMap.html",{"exif":r})

		dajax.assign("#exif","innerHTML",table)
		dajax.assign("#exifError","innerHTML","")
	except Exception as e:
		dajax.assign("#exifError","innerHTML",formatException(e))

	return dajax.json()
	

@dajaxice_register
@login_required
def mailRelation(request,cloudItem,tokenID):

	dajax = Dajax()

	try:
		t = parseAjaxParam(tokenID)
		ci = checkCloudItem(cloudItem,request.user.id)
		tkn = checkAccessToken(t,ci)

		mc = MapsController(tkn)
		res = mc.mailFinder()
	
		table = render_to_string("dashboard/maps/mailRelation.html",{'relation':res})

		dajax.assign("#relation","innerHTML",table)
		dajax.assign("#relationError","innerHTML","")
	except Exception as e:
		dajax.assign("#relationError","innerHTML",formatException(e))

	return dajax.json()
