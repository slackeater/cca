import googledrive, drop
import md5,base64,sys,os,pickle,time,math
from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register
from dajaxice.utils import deserialize_form
from django.utils.html import strip_tags
from forms import MetaSearch,EmailSearch
from django.conf import settings
from downloader.models import AccessToken,FileDownload
from clouditem.models import CloudItem
from django.contrib.auth.models import User
from webapp.func import *
from webapp.exceptionFormatter import formatException
from googledrive import GoogleAnalyzer
from drop import DropboxAnalyzer
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required

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
@login_required
def searchMetaData(request,form,tokenID,cloudItem,start,formType = 1):
	""" Make a search through the metadata """

	dajax = Dajax()

	try:
		t = parseAjaxParam(tokenID)
		ciChk = checkCloudItem(cloudItem,request.user.id)
		tknObj = checkAccessToken(t,ciChk)
		platform = tknObj.serviceType

		f = None

		if int(formType) == 1:
			f = MetaSearch(deserialize_form(form))
		elif int(formType) == 2:
			f = EmailSearch(deserialize_form(form))

		print formType
		print f

		searchStep = 100

		if f.is_valid():
			startResTime = time.time()

			if platform == "google":
				ga = GoogleAnalyzer(tknObj)

				if isinstance(f,MetaSearch):
					res = ga.metadataSearch(int(f.cleaned_data['resType'][0]),int(f.cleaned_data['mimeType']),f.cleaned_data['startDate'],f.cleaned_data['endDate'])
				elif isinstance(f,EmailSearch):
					print "ESEARCH"
					res = ga.emailSearch(f.cleaned_data['email'])
			elif platform == "dropbox":
				d = DropboxAnalyzer(tknObj)

				if isinstance(f,MetaSearch):
					res = d.metadataSearch(int(f.cleaned_data['resType'][0]),int(f.cleaned_data['mimeType']),f.cleaned_data['startDate'],f.cleaned_data['endDate'])
				else:
					raise Exception("This kind of search is not supported for Dropbox.")

			#computation for pager
			totalPages = int(math.ceil(float(len(res))/100.0))
			resultsSlice = res[start:(start+searchStep)]

			stopResTime = time.time()

			parsedTable = render_to_string("dashboard/cloudservice/searchTable.html", {'data': resultsSlice,'totalPages':range(totalPages),'totalRes':len(res),'resTime': stopResTime-startResTime,'platform':platform})

			dajax.assign("#searchRes","innerHTML",parsedTable)
			dajax.assign("#searchError","innerHTML","")
			dajax.remove_css_class("#searchError",['alert','alert-danger'])
		else:
			dajax.assign("#searchError","innerHTML","Please fill all fields")
			dajax.add_css_class("#searchError",['alert','alert-danger'])
	except Exception as e:
		dajax.assign("#searchError","innerHTML",formatException(e))
		dajax.add_css_class("#searchError",['alert','alert-danger'])

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
