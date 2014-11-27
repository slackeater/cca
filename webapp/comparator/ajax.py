from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register
from dajaxice.utils import deserialize_form
from webapp.func import *
from webapp.exceptionFormatter import formatException
import fileComparator
from downloader.models import FileDownload, Download
from django.template.loader import render_to_string
from django.utils.html import strip_tags,strip_entities
import time,sys,traceback

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

		#compute the diff
		info = fileComparator.compareTwo(str(revOne),str(revTwo),f,download.folder,tkn)
		
		imgMimeList = ['image/jpeg','image/png','image/gif','image/bmp']
		table = render_to_string("dashboard/timeliner/diffViewer.html",{'fileName': f.fileName,'revOne': strip_tags(strip_entities(revOne)),'revTwo': strip_tags(strip_entities(revTwo)),'info': info,'imgMimes': imgMimeList})
		
		dajax.assign("#comparator","innerHTML",table)
		dajax.assign("#comparatorError","innerHTML","")
	except Exception as e:
		dajax.assign("#comparatorError","innerHTML",formatException(e))

	return dajax.json()
