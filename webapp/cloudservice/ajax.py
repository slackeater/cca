import googledrive, drop
import md5,base64,sys,os,pickle,time
from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register
from dajaxice.utils import deserialize_form
from django.utils.html import strip_tags
from forms import MetaSearch
from django.conf import settings
from downloader.models import AccessToken,FileDownload
from clouditem.models import CloudItem
from django.contrib.auth.models import User
from webapp.func import *
from webapp.exceptionFormatter import formatException
from googledrive import GoogleAnalyzer
from drop import DropboxAnalyzer

@dajaxice_register
def metadataAnalysis(request,tokenID,cloudItem):
	""" Analyise the metadata of services """

	if not isAuthenticated(request):
		return None

	dajax = Dajax()

	try:
		parsedTable = None
		t = parseAjaxParam(tokenID)
		ciChk = checkCloudItem(cloudItem,request.user.id)
		tknObj = checkAccessToken(t,ciChk)
		platform = tknObj.serviceType

		if platform == "google":
			ga = GoogleAnalyzer(tknObj)
			parsedTable = ga.metadataAnalysis()
		elif platform == "dropbox":
			d = DropboxAnalyzer(tknObj)
			parsedTable = d.metadataAnalysis()

		dajax.assign("#metaAnalysis","innerHTML", parsedTable)
		dajax.assign("#metaAnalysisError","innerHTML","")
	except Exception as e:
		dajax.assign("#metaAnalysisError","innerHTML",formatException(e))

	return dajax.json()


@dajaxice_register
def searchMetaData(request,form,tokenID,cloudItem):
	""" Make a search through the metadata """

	if not isAuthenticated(request):
		return None

	dajax = Dajax()

	try:
		t = parseAjaxParam(tokenID)
		ciChk = checkCloudItem(cloudItem,request.user.id)
		tknObj = checkAccessToken(t,ciChk)
		platform = tknObj.serviceType
		f = MetaSearch(deserialize_form(form))

		if f.is_valid():
			if platform == "google":
				ga = GoogleAnalyzer(tknObj)
				parsedTable = ga.textualMetadataSearch(int(f.cleaned_data['resType'][0]),int(f.cleaned_data['mimeType']),None,None)
			elif platform == "dropbox":
				d = DropboxAnalyzer(tknObj)
				parsedTable = d.textualMetadataSearch(int(f.cleaned_data['resType'][0]),int(f.cleaned_data['mimeType']),None,None)
			
			dajax.assign("#searchRes","innerHTML",parsedTable)
			dajax.assign("#searchError","innerHTML","")
		else:
			dajax.assign("#searchError","innerHTML","Please fill all fields")
	except Exception as e:
		dajax.assign("#searchError","innerHTML",formatException(e))

	return dajax.json()

@dajaxice_register
def fileInfo(request,tokenID,id,cloudItem):
	""" Get the information of a file """

	if not isAuthenticated(request):
		return None
	
	dajax = Dajax()


	try:
		parsedTable = None
		t = parseAjaxParam(tokenID)
		ciChk = checkCloudItem(cloudItem,request.user.id)
		tknObj = checkAccessToken(t,ciChk)
		platform = tknObj.serviceType

		if platform == "google":
			ga = GoogleAnalyzer(tknObj)
			parsedTable = ga.fileInfo(id)
		elif platform == "dropbox":
			d = DropboxAnalyzer(tknObj)
			parsedTable = d.fileInfo(id)

		dajax.assign("#fileRevisionContainer","innerHTML",parsedTable)
		dajax.assign("#searchError","innerHTML","")
	except Exception as e:
		dajax.assign("#searchError","innerHTML",formatException(e))

	return dajax.json()

@dajaxice_register
def fileRevision(request,fId,tokenID,cloudItem):

	if not isAuthenticated(request):
		return None

	dajax = Dajax()


	try:
		parsedTable = None
		t = parseAjaxParam(tokenID)
		ciChk = checkCloudItem(cloudItem,request.user.id)
		tknObj = checkAccessToken(t,ciChk)
		platform = tknObj.serviceType
		
		if platform == "google":
			ga = GoogleAnalyzer(tknObj)
			parsedTable = ga.fileHistory(fId)
		elif platform == "dropbox":
			d = DropboxAnalyzer(tknObj)
			parsedTable = d.fileHistory(fId)
		
		dajax.assign("#revisionHistory","innerHTML",parsedTable)
		dajax.assign("#searchError","innerHTML","")
	except Exception as e:
		dajax.assign("#searchError","innerHTML",formatException(e))

	return dajax.json()
