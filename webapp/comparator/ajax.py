from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register
from dajaxice.utils import deserialize_form
from webapp.func import *
import fileComparator
from downloader.models import FileDownload
from django.template.loader import render_to_string
import time
@dajaxice_register
def compareTwoFile(request,revOne,revTwo,altName,cloudItem,tokenID):
	
	if not isAuthenticated(request):
		return None

	dajax = Dajax()

	try:
		t = parseAjaxParam(tokenID)
		ci = checkCloudItem(cloudItem,request.user.id)
		tkn = checkAccessToken(t,ci)
	
		#get file alternate name from db
		altNameDb = FileDownload.objects.get(tokenID=tkn,alternateName=altName)

		fileComparator.compareTwo(revOne,revTwo,altNameDb.alternateName,tkn)
		
		iframe = "<iframe id='viewer' src ='/static/diff/diff.pdf' height='600' width='800' style='text-align: center'  allowfullscreen webkitallowfullscreen></iframe>"
		dajax.assign("#comparator","innerHTML",iframe)
	except:
		dajax.assign("#comparatorError","innerHTML",e.message)

	return dajax.json()
