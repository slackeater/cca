from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register
from webapp.func import *
from django.template.loader import render_to_string
import timemaker

@dajaxice_register
def documentsTimeliner(request,cloudItem,tokenID):

	if not isAuthenticated(request):
		return None

	dajax = Dajax()
	
	try:
		t = parseAjaxParam(tokenID)
		ci = checkCloudItem(cloudItem,request.user.id)
		tkn = checkAccessToken(t,ci)
		data = timemaker.docmentsHistoryTimeline(ci,tkn)
		print data
		table = render_to_string("dashboard/timeliner/historytimeline.html",{'events':data})	
		print table
		dajax.assign("#timeHistory","innerHTML",table)
	except Exception as e:
		dajax.assign("#timeHistoryError","innerHTML",e.message)

	return dajax.json()


