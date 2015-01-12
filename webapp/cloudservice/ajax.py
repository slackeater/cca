import md5,base64,sys,os,pickle,time,math
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
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from webapp.metadataController import MetadataController
import webapp.crypto

@dajaxice_register
@login_required
def metadataAnalysis(request,tokenID,cloudItem):
	""" Analyise the metadata of services """

	dajax = Dajax()

	try:
		parsedTable = None
		t = parseAjaxParam(tokenID)
		ciChk = checkCloudItem(cloudItem,request.user.id)
		tknObj = checkAccessToken(t,ciChk)

		mc = MetadataController(tknObj)
		parsedTable = mc.metadataAnalysis()

		dajax.assign("#metaAnalysis","innerHTML", parsedTable)
		dajax.assign("#metaAnalysisError","innerHTML","")
	except Exception as e:
		dajax.assign("#metaAnalysisError","innerHTML",formatException(e))

	return dajax.json()


@dajaxice_register
@login_required
def searchMetaData(request,form,tokenID,cloudItem,start):
	""" Make a search through the metadata """

	dajax = Dajax()

	try:
		t = parseAjaxParam(tokenID)
		ciChk = checkCloudItem(cloudItem,request.user.id)
		tknObj = checkAccessToken(t,ciChk)
		searchStep = 100
		f = MetaSearch(deserialize_form(form))

		if f.is_valid():
			startResTime = time.time()
			#compute hash of the search form for the cache
			searchHash = crypto.sha256(form).hexdigest()
			"""searchHash = crypto.sha256(f.cleaned_data['formType'][0]+crypto.HASH_SEPARATOR+
					f.cleaned_data['email']+crypto.HASH_SEPARATOR+
					f.cleaned_data['filename']+crypto.HASH_SEPARATOR+
					f.cleaned_data['givenname']+crypto.HASH_SEPARATOR+
					f.cleaned_data['resType'][0]+crypto.HASH_SEPARATOR+
					f.cleaned_data['mimeType']+crypto.HASH_SEPARATOR+
					str(f.cleaned_data['startDate'])+crypto.HASH_SEPARATOR+
					str(f.cleaned_data['endDate'])
				).hexdigest()"""

			if "searchCache" in request.session and request.session['searchCacheID'] == searchHash:
				res = json.loads(request.session["searchCache"])
			else:
				mc = MetadataController(tknObj)
				res = mc.metadataSearch(
						int(f.cleaned_data['formType'][0]),
						f.cleaned_data['email'],
						f.cleaned_data['filename'],
						f.cleaned_data['givenname'],
						int(f.cleaned_data['resType'][0]),
						int(f.cleaned_data['mimeType']),
						f.cleaned_data['startDate'],
						f.cleaned_data['endDate']
					)

				request.session["searchCacheID"] = searchHash
				request.session["searchCache"] = json.dumps(res)

			#computation for pager
			totalPages = int(math.ceil(float(len(res))/100.0))
			resultsSlice = res[start:(start+searchStep)]

			stopResTime = time.time()

			parsedTable = render_to_string("dashboard/cloudservice/searchTable.html", {'data': resultsSlice,'totalPages':range(totalPages),'totalRes':len(res),'resTime': stopResTime-startResTime,'platform':tknObj.serviceType})

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
@login_required
def fileInfo(request,tokenID,id,cloudItem):
	""" Get the information of a file """

	dajax = Dajax()

	try:
		parsedTable = None
		t = parseAjaxParam(tokenID)
		ciChk = checkCloudItem(cloudItem,request.user.id)
		tknObj = checkAccessToken(t,ciChk)

		mc = MetadataController(tknObj)
		parsedTable = mc.fileInfo(id)

		dajax.assign("#fileRevisionContainer","innerHTML",parsedTable)
		dajax.assign("#searchError","innerHTML","")
	except Exception as e:
		dajax.assign("#searchError","innerHTML",formatException(e))

	return dajax.json()

@dajaxice_register
@login_required
def fileRevision(request,fId,tokenID,cloudItem):

	dajax = Dajax()

	try:
		parsedTable = None
		t = parseAjaxParam(tokenID)
		ciChk = checkCloudItem(cloudItem,request.user.id)
		tknObj = checkAccessToken(t,ciChk)

		mc = MetadataController(tknObj)
		parsedTable = mc.fileHistory(fId)

		dajax.assign("#revisionHistory","innerHTML",parsedTable)
		dajax.assign("#searchError","innerHTML","")
	except Exception as e:
		dajax.assign("#searchError","innerHTML",formatException(e))

	return dajax.json()
