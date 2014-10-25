from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register, dajaxice_functions
from django.conf import settings
import sys, os, json

# add path for crypto
cryptoPath = os.path.join(os.path.dirname(settings.BASE_DIR), "finder")

if not cryptoPath in sys.path:
	sys.path.insert(1, cryptoPath)
del cryptoPath

import crypto

@dajaxice_register
def decrypt(request):
	dajax = Dajax()
	fileName = request.session['fileName']
	fileCont = open(os.path.join("/tmp",fileName), "r")
	print json.load(fileCont)
	print crypto.sha256("ciao")
	return dajax.json()

