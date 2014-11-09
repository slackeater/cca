import googledrive, drop
import md5,base64,sys
from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register
from dajaxice.utils import deserialize_form
from forms import MetaSearch

def isAuhtenticated(request):
	""" Check if a user is authenticated """
	return request.user.is_authenticated()

def initCheck(request,tokenID = None):

	auth = False
	t = 0

	# check authentication	
	auth = isAuhtenticated(request)

	if not auth:
		sys.exit("Authentication requires")

	t = int(tokenID)

	if not t > 0:
		sys.exit("Invalid token parameters")
	
	return auth,t


@dajaxice_register
def metadataAnalysis(request,tokenID, update, platform):
	""" Analyise the metadata of services """

	auth,t = initCheck(request,tokenID)

	dajax = Dajax()

	parsedTable = None

	try:
		if platform == "google":
			parsedTable = googledrive.metadataAnalysis(request, update, t)
		elif platform == "dropbox":
			parsedTable = drop.metadataAnalysis(request,update,t)

		dajax.assign("#metaAnalysis","innerHTML", parsedTable)
		dajax.assign("#metaAnalysisError","innerHTML","")
	except Exception as e:
		dajax.assign("#metaAnalysisError","innerHTML",e)

	return dajax.json()

@dajaxice_register
def userInfo(request,tokenID,platform):
	""" Show user info """

	auth,t = initCheck(request,tokenID)

	dajax = Dajax()

	parsedTable = None

	try:
		if platform == "google":
			parsedTable = googledrive.userInformation(request,t)
		elif platform == "dropbox":
			parsedTable = drop.userInformation(request,t)
				
		dajax.assign("#accountTab","innerHTML",parsedTable)
		dajax.assign("#userInfoError","innerHTML","")
	except (Exception,TypeError) as e:
		dajax.assign("#userInfoError","innerHTML",e)

	return dajax.json()

@dajaxice_register
def searchMetaData(request,platform,form,tokenID):
	auth,t = initCheck(request,tokenID)

	dajax = Dajax()

	try:
		f = MetaSearch(deserialize_form(form))

		if f.is_valid():
			if platform == "google":
				parsedTable = googledrive.metadataSearch(t,int(f.cleaned_data['resType'][0]),int(f.cleaned_data['mimeType']))
			elif platform == "dropbox":
				parsedTable = drop.metadataSearch(t,int(f.cleaned_data['resType'][0]),int(f.cleaned_data['mimeType']))
			
			dajax.assign("#searchRes","innerHTML",parsedTable)
			dajax.assign("#searchError","innerHTML","")
		else:
			dajax.assign("#searchError","innerHTML","Please fill all fields")
	except Exception as e:
		dajax.assign("#searchError","innerHTML",e)

	return dajax.json()

@dajaxice_register
def fileInfo(request,platform,tokenID,id):

	auth,t = initCheck(request,tokenID)

	dajax = Dajax()

	parsedTable = None

	try:
		if platform == "google":
			parsedTable = googledrive.fileInfo(t,id)
		elif platform == "dropbox":
			parsedTable = drop.fileInfo(t,id)

		dajax.assign("#fileRevisionContainer","innerHTML",parsedTable)
		dajax.assign("#searchError","innerHTML","")
	except Exception as e:
		dajax.assign("#searchError","innerHTML",e)

	return dajax.json()

@dajaxice_register
def fileRevision(request,platform,id,tokenID):

	auth,t = initCheck(request,tokenID)

	dajax = Dajax()

	parsedTable = None

	try:
		sessionCredentials = request.session[md5.new(str(tokenID)).hexdigest()]

		if platform == "google":
			parsedTable = googledrive.fileHistory(id,sessionCredentials)
		elif platform == "dropbox":
			parsedTable = drop.fileHistory(id,sessionCredentials)
		
		dajax.assign("#revisionHistory","innerHTML",parsedTable)
		dajax.assign("#searchError","innerHTML","")
	except Exception as e:
		dajax.assign("#searchError","innerHTML",e)

	return dajax.json()

@dajaxice_register
def showDownload(request, tokenID,platform):
	""" Show the download size """

	auth, t = initCheck(request,tokenID)

	dajax = Dajax()

	parsedTable = None

	try:
		if platform == "google":
			parsedTable = googledrive.downloadSize(t)
		elif platform == "dropbox":
			parsedTable = drop.downloadSize(t)

		dajax.assign("#downCont","innerHTML",parsedTable)
		dajax.assign("#downError","innerHTML","")
	except Exception as e:
		dajax.assign("#downError","innerHTML",e)

	return dajax.json()


@dajaxice_register
def initDownload(request, platform, tokenID):
	""" Initialize a download """
