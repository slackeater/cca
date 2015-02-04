from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register
from dajaxice.utils import deserialize_form
from webapp.func import *
from webapp.databaseInterface import DbInterface
from webapp.exceptionFormatter import formatException
from comparator.fileComparator import Comparator
from downloader.models import FileDownload, Download
from django.template.loader import render_to_string
from django.utils.html import strip_tags,strip_entities
import time,sys,traceback
from webapp import constConfig
from forms import VerifyForm
from dajaxice.utils import deserialize_form
from django.contrib.auth.decorators import login_required
from comparator.fileVerifier import Verifier

@dajaxice_register
@login_required
def compareTwoFile(request,revOne,revTwo,altName,cloudItem,tokenID):
	""" Compare two file by using two revisions """

	dajax = Dajax()

	try:
		t = parseAjaxParam(tokenID)
		ci = checkCloudItem(cloudItem,request.user.id)
		tkn = checkAccessToken(t,ci)
	
		#compute the diff
		c = Comparator(tkn)
		info = c.compareTwo(str(revOne),str(revTwo),altName)
		
		imgMimeList = ['image/jpeg','image/png','image/gif','image/bmp']
		table = render_to_string("dashboard/timeliner/diffViewer.html",{'fileName': info["filename"],'revOne': strip_tags(strip_entities(revOne)),'revTwo': strip_tags(strip_entities(revTwo)),'info': info,'imgMimes': imgMimeList})
		
		dajax.assign("#comparator","innerHTML",table)
		dajax.assign("#comparatorError","innerHTML","")
	except Exception as e:
		dajax.assign("#comparatorError","innerHTML",formatException(e))

	return dajax.json()
			
@dajaxice_register
@login_required
def verifyFile(request,cloudItem,tokenID,form):
	""" Verify file and metadata """

	dajax = Dajax()

	try:
		t = parseAjaxParam(tokenID)
		ci = checkCloudItem(cloudItem,request.user.id)
		tkn = checkAccessToken(t,ci)
		f = VerifyForm(deserialize_form(form))

		if f.is_valid():

			verType = parseAjaxParam(f.cleaned_data['verificationType'])
			metaVerification = None
			downVerification = None
			dtaVerification = None
			v = Verifier(tkn)

			if verType == constConfig.VERIFY_CHOICE_METADATA:
				metaVerification = v.verifyMetadata()
			elif verType == constConfig.VERIFY_CHOICE_FILES or verType == constConfig.VERIFY_CHOICE_FILESHISTORY:
				downVerification = v.verifyFileDownload(verType)
			elif verType == constConfig.VERIFY_CHOICE_DTA_SIGNATURE:
				dtaVerification = v.verifyZIP()
				
			else:
				raise Exception ("Invalid Verification Type")

			table = render_to_string("dashboard/comparator/comparatorVerify.html",{"meta":metaVerification,'file': downVerification,'dta':dtaVerification})

			dajax.assign("#verifyer","innerHTML",table)
			dajax.assign("#verifyerError","innerHTML","")
			dajax.remove_css_class("#verifyerError",['alert','alert-danger'])
		else:
			dajax.assign("#verifyer","innerHTML","")
			dajax.assign("#verifyerError","innerHTML","Invalid Form")
			dajax.add_css_class("#verifyerError",['alert','alert-danger'])
	except Exception as e:
		dajax.assign("#verifyerError","innerHTML",formatException(e))
		dajax.add_css_class("#verifyerError",['alert','alert-danger'])

	return dajax.json()

@dajaxice_register
@login_required
def compareFromReport(request,cloudItem,tokenID):
	""" Compare files using the previously imported report """

	dajax = Dajax()

	try:
		t = parseAjaxParam(tokenID)
		ci = checkCloudItem(cloudItem,request.user.id)
		tkn = checkAccessToken(t,ci)
		
		c = Comparator(tkn)
		res = c.compareFromReport()

		table = render_to_string("dashboard/comparator/comparatorCompare.html",{'files':res})

		dajax.assign("#comparator","innerHTML",table)
		dajax.assign("#comparatorError","innerHTML","")
		dajax.remove_css_class("#comparatorError",['alert','alert-danger'])
	except Exception as e:
		dajax.assign("#comparatorError","innerHTML",formatException(e))
		dajax.add_css_class("#comparator",['alert','alert-danger'])

	return dajax.json()

@dajaxice_register
@login_required
def displaySingle(request,cloudItem,tokenID,title,altName,downAltName,fileType):
	""" Compare files using the previously imported report """

	dajax = Dajax()

	try:
		t = parseAjaxParam(tokenID)
		ci = checkCloudItem(cloudItem,request.user.id)
		tkn = checkAccessToken(t,ci)
		
                c = Comparator(tkn)
                res = c.displaySingle(title,altName,downAltName,fileType)
                res.update({'imgMimes':constConfig.ALLOWED_MIME_TYPE[1:-1]})
		table = render_to_string("dashboard/timeliner/singleViewer.html",res)
                dajax.assign("#comparator","innerHTML",table)
		dajax.assign("#comparatorError","innerHTML","")
	except Exception as e:
		dajax.assign("#comparatorError","innerHTML",formatException(e))
		dajax.add_css_class("#comparator",['alert','alert-danger'])

	return dajax.json()




