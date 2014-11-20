from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register
from dajaxice.utils import deserialize_form
from webapp.func import *
from django.template.loader import render_to_string
import droptimemaker,googletimemake
from cloudservice.forms import MetaSearch

@dajaxice_register
def formTimeliner(request,cloudItem,tokenID,form):

	if not isAuthenticated(request):
		return None

	dajax = Dajax()
	data = None

	try:
		t = parseAjaxParam(tokenID)
		ci = checkCloudItem(cloudItem,request.user.id)
		tkn = checkAccessToken(t,ci)
		f = MetaSearch(deserialize_form(form))

		if f.is_valid():
			if tkn.serviceType == "google":
				data = googletimemaker.formTimeline(ci,tkn,int(f.cleaned_data['resType'][0]),f.cleaned_data['mimeType'])
			elif tkn.serviceType == "dropbox":
				data = droptimemaker.formTimeline(ci,tkn,int(f.cleaned_data['resType'][0]),f.cleaned_data['mimeType'])

			table = render_to_string("dashboard/timeliner/historytimeline.html",{'events':data})	
			dajax.assign("#formHistory","innerHTML",table)
		else:
			raise Exception("Invalid form")
			
	except Exception as e:	
		dajax.assign("#formHistoryError","innerHTML",e.message)
	
	return dajax.json()

@dajaxice_register
def fileHistoryTimeliner(request,cloudItem,tokenID,altName):

	if not isAuthenticated(request):
		return None

	dajax = Dajax()
	data = None

	try:
		t = parseAjaxParam(tokenID)
		ci = checkCloudItem(cloudItem,request.user.id)
		tkn = checkAccessToken(t,ci)

		data = timemaker.filehistoryTimeline(ci,t,altName)

		#check that we have at least one item
		if len(data) > 0:
			ft = FileDownload.objects.get(alternateName=altName,tokenID=t).fileName
			table = render_to_string("dashboard/timeliner/filehistorytimeline.html",{'events':data,'fileTitle':ft})	
			dajax.assign("#fileHistory","innerHTML",table)
		else:
			raise Exception("No history for this file")
	except Exception as e:	
		dajax.assign("#formHistoryError","innerHTML",e.message)

	return dajax.json()
