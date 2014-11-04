from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register
import oauth, sys, dropbox
import json
from models import DropboxToken
from importer.models import Upload


@dajaxice_register
def submitDropboxCode(request, code, impID):
	""" Submit the dropbox authorization code """
	return submitCode(request, code, impID, "dropbox")

@dajaxice_register
def submitGoogleCode(request, code, impID):
	""" Submit the dropbox authorization code """
	return submitCode(request, code, impID, "google")

def submitCode(request, code, impID, platform):
	""" Get the access code from the code """

	if not request.user.is_authenticated():
		sys.exit("Auth required")

	dajax = Dajax()
	eID = "#gStat" if platform == "google" else "#dStat"
	
	try:
		if code is None:
			raise Exception("Invalid code")

		if platform == "google":
			token = oauth.googleAccessToken(code)
			print >> sys.stderr, str(token.to_json())
		elif platform == "dropbox":
			token = oauth.dropboxAccessToken(code)
			dropTkn = DropboxToken(importID=Upload.objects.get(id=impID), accessToken=token[0], userID=token[1])
			dropTkn.save()
			dajax.assign(eID,"innerHTML",str("Access Token: " + token[0] + "<br />User ID: " + token[1]))
		else: 
			raise Exception("Invalid platform")

	except dropbox.rest.ErrorResponse as e:
		dajax.assign(eID,"innerHTML",str(e.status) + ", " + str(e.reason) + ", " + str(e.error_msg))
	#except Exception as e:
	#	dajax.assign(eID,"innerHTML", str(e.message))
	
	return dajax.json()
