from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register
from dajaxice.utils import deserialize_form
from webapp.func import *
import fileComparator
from downloader.models import FileDownload, Download
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
	
		#get file alternate name and file name from db
		f = FileDownload.objects.get(tokenID=tkn,alternateName=altName)

		#get folder name
		download = Download.objects.get(tokenID=tkn,threadStatus="completed")

		diffName = fileComparator.compareTwo(str(revOne),str(revTwo),f,download.folder,tkn)
		
		iframe = "<embed src ='/diff/"+diffName+"' height='600' width='100%' style='text-align: center'>"
		
		dajax.assign("#comparator","innerHTML",iframe)
	except Exception as e:
		dajax.assign("#comparatorError","innerHTML",e.message)

	return dajax.json()
