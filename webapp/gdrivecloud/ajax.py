from dajax.core import Dajax
from django.conf import settings
from dajaxice.decorators import dajaxice_register
import json, os, sys, base64, pickle, StringIO
from models import GoogleFileMetadata
from dashboard.models import GoogleDriveToken
import drive
from importer.models import Upload
from django.template.loader import render_to_string
from dajaxice.utils import deserialize_form

def isAuthenticated(request):
	""" Check if a user is authenticated """
	return request.user.is_authenticated()

@dajaxice_register
def analyzeMetaData(request, tokenID, importID, update):
	dajax = Dajax()

	# check authenticaton
	if not isAuthenticated(request):
		return None

	try:
		sessionName = "session"+str(int(importID))+"-"+str(int(tokenID))
		parsedTable = drive.metadataAnalysis(request, sessionName, update, int(tokenID))
		dajax.assign("#metaAnalysis", "innerHTML", parsedTable)
	except Exception as e:
		dajax.assign("#metaAnalysisError","innerHTML", e)

	return dajax.json()
