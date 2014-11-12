from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register, dajaxice_functions
from django.conf import settings
import sys, os, json, zipfile
from models import Upload
from webapp.func import isAuthenticated, parseAjaxParam
# add path for crypto
cryptoPath = os.path.join(os.path.dirname(settings.BASE_DIR), "finder")

if not cryptoPath in sys.path:
	sys.path.insert(1, cryptoPath)
del cryptoPath

import crypto

@dajaxice_register
def showReport(request,up,ci):
	if not isAuthenticated(request):
		return None

	dajax = Dajax()

	#check that the import belong to the clouditem
	#TODO
	
