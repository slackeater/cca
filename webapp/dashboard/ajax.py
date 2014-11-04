from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register
import drop, sys
import json
from models import DropboxToken
from importer.models import Upload


@dajaxice_register
def submitDropboxCode(request, code, impID):
	""" Submit the dropbox authorization code """

	if not request.user.is_authenticated():
		sys.exit("Auth required")

	dajax = Dajax()
	
	try:
		token = drop.accessToken(code)
		dropTkn = DropboxToken(importID=Upload.objects.get(id=impID), accessToken=token[0], userID=token[1])
		dropTkn.save()
		dajax.assign("#stat","innerHTML",str("Access Token: " + token[0] + "<br />User ID: " + token[1]))
	except dropbox.rest.ErrorResponse as e:
		dajax.assign("#stat","innerHTML",str(e.status) + ", " + str(e.reason) + ", " + str(e.error_msg))
	except Exception as e:
		dajax.assign("#stat","innerHTML", str(e.message))
	return dajax.json()
