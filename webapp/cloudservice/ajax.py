import googledrive, drop
import md5,base64,sys,os,pickle,time
from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register
from dajaxice.utils import deserialize_form
from django.utils.html import strip_tags
from forms import MetaSearch
from django.conf import settings
from models import Downloads
from googleapiclient.discovery import Resource

def isAuhtenticated(request):
	""" Check if a user is authenticated """
	return request.user.is_authenticated()

def initCheck(request,tokenID):

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
def startForegroundDownload(request, platform, tokenID):
	""" Initialize a download """

	auth, t = initCheck(request,tokenID)

	#check if there is already a folder
	fName = md5.new(str(t)).hexdigest()
	downFolder = os.path.join(settings.DOWNLOAD_DIR,fName)
	dajax = Dajax()

	#if the folder exists or is not empty return
	if os.path.isdir(downFolder) and os.listdir(downFolder) != []:
		dajax.assign("#status","innerHTML","false")
		dajax.assign("#downError","innerHTML","A folder already exists with the same name / folder not empty")
	else:
		try:
			if not os.path.isdir(downFolder):
				os.mkdir(downFolder)
				
			dbDir, created = Downloads.objects.get_or_create(dirName=downFolder,defaults={'dirName':downFolder,'status':0})

			if dbDir.status == 0 and (platform == "google" or platform == "dropbox"):
				dajax.assign("#status","innerHTML","true")
				dajax.assign("#p","value",platform)
			else:
				dajax.assign("#downError","innerHTML","Error")
		except (Error,Exception) as e:
			dajax.assign("#downError","innerHTML",e.message)

	return dajax.json()

@dajaxice_register
def downloadFile(request,platform,tokenID,fileID):
	""" Download a file """

	auth, t = initCheck(request, tokenID)
	dajax = Dajax()
	
	try:
		sName = md5.new(str(t)).hexdigest()
		sessionData = request.session[sName]

		if platform == "google":
			status, fName = googledrive.downloadFile(strip_tags(fileID),sessionData,t)
			time.sleep(5)

		elif platform == "dropbox":
			status = False
			
		if status:
			dajax.assign("#status","innerHTML","correct")
			dajax.assign("#fID","innerHTML",fName)
		else:
			dajax.assign("#status","innerHTML","incorrect")
			dajax.assign("#fID","innerHTML",fName)
	except:
		e = sys.exc_info()
		lineno = e[-1].tb_lineno
		dajax.assign("#status","innerHTML", str(e) + " at line " + str(lineno))

	return dajax.json()


