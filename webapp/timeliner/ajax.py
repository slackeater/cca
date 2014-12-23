from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register
from dajaxice.utils import deserialize_form
from webapp.func import *
from django.template.loader import render_to_string
import droptimemaker,googletimemake
from cloudservice.forms import MetaSearch
from webapp.timelinerController import TimelinerController
from webapp.exceptionFormatter import formatException
from django.contrib.auth.decorators import login_required

@dajaxice_register
@login_required
def formTimeliner(request,cloudItem,tokenID,form):

	dajax = Dajax()

	try:
		t = parseAjaxParam(tokenID)
		ci = checkCloudItem(cloudItem,request.user.id)
		tkn = checkAccessToken(t,ci)
		f = MetaSearch(deserialize_form(form))

		if f.is_valid():
			tc = TimelinerController(tkn) 
			data = tc.formTimeLine(
					int(f.cleaned_data['formType'][0]),
					f.cleaned_data['email'],
					f.cleaned_data['filename'],
					f.cleaned_data['givenname'],
					int(f.cleaned_data['resType'][0]),
					f.cleaned_data['mimeType'],
					f.cleaned_data['startDate'],
					f.cleaned_data['endDate']
			)
			
			if len(data) > 0:
				if len(data) > 500:
					dajax.assign("#formHistoryError","innerHTML","Your query returned more than 500 elements. Please refine your search to avoid performance problems with your browser.")
					dajax.add_css_class("#formHistoryError",["alert","alert-danger"])
				else:
					table = render_to_string("dashboard/timeliner/historytimeline.html",{'events':data})	
					dajax.assign("#formHistory","innerHTML",table)
					dajax.assign("#formHistoryError","innerHTML","")
					dajax.remove_css_class("#formHistoryError",["alert","alert-danger"])
			else:
				dajax.assign("#formHistoryError","innerHTML","No data found.")
				dajax.add_css_class("#formHistoryError",["alert","alert-danger"])
		else:
			dajax.assign("#formHistoryError","innerHTML","Invalid Form")
			dajax.add_css_class("#formHistoryError",["alert","alert-danger"])
			
	except Exception as e:	
		dajax.assign("#formHistoryError","innerHTML",formatException(e))
		dajax.add_css_class("#formHistoryError",["alert","alert-danger"])
	
	return dajax.json()

@dajaxice_register
@login_required
def fileHistoryTimeliner(request,cloudItem,tokenID,altName):

	dajax = Dajax()

	try:
		t = parseAjaxParam(tokenID)
		ci = checkCloudItem(cloudItem,request.user.id)
		tkn = checkAccessToken(t,ci)
		tc = TimelinerController(tkn)
		data = tc.fileHistoryTimeLine(altName)

		#check that we have at least one item
		if len(data) > 0:
			ft = FileDownload.objects.get(alternateName=altName,tokenID=t).fileName
			table = render_to_string("dashboard/timeliner/filehistorytimeline.html",{'events':data,'fileTitle':ft,'altName': altName})	
			dajax.assign("#fileHistory","innerHTML",table)
			dajax.assign("#formHistoryError","innerHTML","")
		else:
			raise Exception("No history for this file")
	except Exception as e:	
		dajax.assign("#formHistoryError","innerHTML",formatException(e))

	return dajax.json()
