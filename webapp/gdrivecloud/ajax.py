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
from dropcloud.forms import DropMetaSearch
from django.utils.html import strip_tags

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

@dajaxice_register
def searchMetaData(request, form, tokenID):
	""" Search through the metadata """
	
	if not isAuthenticated(request):
		return None

	dajax = Dajax()
	desForm = DropMetaSearch(deserialize_form(form))

	if desForm.is_valid():
		try:
			parsedTable = drive.metadataSearch(int(tokenID), strip_tags(desForm))
			dajax.assign("#searchRes","innerHTML", parsedTable)
			dajax.assign("#searchError", "innerHTML", "")
		except Exception as e:
			dajax.assign("#searchError", "innerHTML", e.message)
	else:
		dajax.assign("#searchError", "innerHTML", "Form is not valid.")

	return dajax.json()

@dajaxice_register
def fileInfo(request, id, tokenID):
	""" Show the info for the requested file """

	if not isAuthenticated(request):
		return None

	dajax = Dajax()
	try:
		parsedTable = drive.fileInfo(int(tokenID), strip_tags(id))
		dajax.assign("#fileRevisionContainer","innerHTML",parsedTable)
	except Exception as e:
		dajax.assign("#searchError","innerHTML",e.message)

	return dajax.json()

@dajaxice_register
def fileRevision(request, id, tokenID, importID):
	""" Show the file history """

	if not isAuthenticated(request):
		return None

	dajax = Dajax()

	try:
		sessionName = "session"+str(int(importID))+"-"+str(int(tokenID))
		parsedTable = drive.fileHistory(id, request.session[sessionName])
		dajax.assign("#revisionHistory","innerHTML",parsedTable)
	except Exception as e:
		dajax.assign("#searchError","innerHTML",e.message)

	return dajax.json()
