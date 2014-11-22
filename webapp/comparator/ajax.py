from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register
from dajaxice.utils import deserialize_form
from webapp.func import *
from django.template.loader import render_to_string

@dajaxice_register
def compareFile(request,cloudItem,tokenID):
	
	if not isAuthenticated(request):
		return None

	dajax = Dajax()

	try:
		t = parseAjaxParam(tokenID)
		ci = checkCloudItem(cloudItem,request.user.id)
		tkn = checkAccessToken(t,ci)
		dajax.assign("#comparator","innerHTML","text")
	except:
		dajax.assign("#comparatorError","innerHTML",e.message)

	return dajax.json()
