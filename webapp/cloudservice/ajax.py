import googledrive, drop
import md5,base64,sys,os,pickle,time
from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register
from dajaxice.utils import deserialize_form
from django.utils.html import strip_tags
from forms import MetaSearch
from django.conf import settings
from models import Downloads
from downloader.models import AccessToken,FileDownload
from clouditem.models import CloudItem
from django.contrib.auth.models import User
from webapp.func import *


@dajaxice_register
def metadataAnalysis(request,tokenID,cloudItem):
	""" Analyise the metadata of services """

	if not isAuthenticated(request):
		return None

	dajax = Dajax()

	parsedTable = None
	
	try:
		t = parseAjaxParam(tokenID)
		ciChk = checkCloudItem(cloudItem,request.user.id)
		tknObj = checkAccessToken(t,ciChk)
		platform = tknObj.serviceType
		print platform

		if platform == "google":
			parsedTable = googledrive.metadataAnalysis(request, t)
		elif platform == "dropbox":
			parsedTable = drop.metadataAnalysis(request,t)

		dajax.assign("#metaAnalysis","innerHTML", parsedTable)
		dajax.assign("#metaAnalysisError","innerHTML","")
	except Exception as e:
		dajax.assign("#metaAnalysisError","innerHTML",e.message)

	return dajax.json()


@dajaxice_register
def searchMetaData(request,form,tokenID,cloudItem):

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
				parsedTable = googledrive.metadataSearch(t,int(f.cleaned_data['resType'][0]),int(f.cleaned_data['mimeType']))
			elif platform == "dropbox":
				parsedTable = drop.metadataSearch(t,int(f.cleaned_data['resType'][0]),int(f.cleaned_data['mimeType']))
			
			dajax.assign("#searchRes","innerHTML",parsedTable)
			dajax.assign("#searchError","innerHTML","")
		else:
			dajax.assign("#searchError","innerHTML","Please fill all fields")
	except Exception as e:
		dajax.assign("#searchError","innerHTML",e)

	return dajax.json()

@dajaxice_register
def fileInfo(request,tokenID,id,cloudItem):


	if not isAuthenticated(request):
		return None
	
	dajax = Dajax()

	parsedTable = None

	try:
		t = parseAjaxParam(tokenID)
		ciChk = checkCloudItem(cloudItem,request.user.id)
		tknObj = checkAccessToken(t,ciChk)
		platform = tknObj.serviceType

		if platform == "google":
			parsedTable = googledrive.fileInfo(t,id)
		elif platform == "dropbox":
			parsedTable = drop.fileInfo(t,id)

		dajax.assign("#fileRevisionContainer","innerHTML",parsedTable)
		dajax.assign("#searchError","innerHTML","")
	except Exception as e:
		dajax.assign("#searchError","innerHTML",e)

	return dajax.json()

@dajaxice_register
def fileRevision(request,fId,tokenID,cloudItem):

	if not isAuthenticated(request):
		return None

	dajax = Dajax()

	parsedTable = None

	try:
		t = parseAjaxParam(tokenID)
		ciChk = checkCloudItem(cloudItem,request.user.id)
		tknObj = checkAccessToken(t,ciChk)
		platform = tknObj.serviceType
		#check that the id belongs to the token ID

		fileDB = FileDownload.objects.get(tokenID=AccessToken.objects.get(id=t),alternateName=fId)

		if platform == "google":
			parsedTable = googledrive.fileHistory(fileDB)
		elif platform == "dropbox":
			parsedTable = drop.fileHistory(fileDB)
		
		dajax.assign("#revisionHistory","innerHTML",parsedTable)
		dajax.assign("#searchError","innerHTML","")
	except Exception as e:
		dajax.assign("#searchError","innerHTML",e)

	return dajax.json()
