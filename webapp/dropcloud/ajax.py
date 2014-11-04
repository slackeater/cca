from dajax.core import Dajax
from django.conf import settings
from dajaxice.decorators import dajaxice_register
import json, os, sys, base64, pickle, StringIO
from models import DropboxFileMetadata
from dashboard.models import DropboxToken
import dropbox
from importer.models import Upload
from django.template.loader import render_to_string
from forms import DropMetaSearch
from dajaxice.utils import deserialize_form

# add path for crypto
cryptoPath = os.path.join(os.path.dirname(settings.BASE_DIR), "finder")

if not cryptoPath in sys.path:
	sys.path.insert(1, cryptoPath)
del cryptoPath

import crypto

@dajaxice_register
def analyzeDropMetaData(request, resName, tokenID):
	""" Download and analyze dropbox metadata """

	checkUserAuthentication(request)

	dajax = Dajax() 
	
	try:
		#get token
		t = DropboxToken.objects.get(id=tokenID)
		c = dropbox.client.DropboxClient(t.accessToken)

		try:
			# check if we already have parsed this tree with the actual token
			getMeta = DropboxFileMetadata.objects.filter(tokenID=t).latest("metaTime")
			metaInfo = pickle.loads(base64.b64decode(getMeta.metadata))
			dajax.assign("#statusMeta","innerHTML", str("Showing analysis of ") + str(getMeta.metaTime))
		except DropboxFileMetadata.DoesNotExist:
			getMeta = None

		data = c.metadata("/", include_deleted=True, include_media_info=True)	

		#get new metadata if we do not have or the hash do not coincide
		if getMeta is None or metaInfo[0]['hash'] != data['hash']:
			dajax.assign("#statusMeta","innerHTML", str("Downloaded from Dropbox now."))
			#parse directory tree
			pickledMetaInfo= StringIO.StringIO()
			metaInfo = recurseDropTree(data, c, 5);
			pickle.dump(metaInfo, pickledMetaInfo)
			
			#store this result
			metastore = DropboxFileMetadata(metadata=base64.b64encode(pickledMetaInfo.getvalue()), tokenID=t)
			metastore.save()

		dirCount, fileSize, fileCount, fileType, deletedFile, deletedDirs = parseDropTree(metaInfo)
		data = { 'dC': dirCount, 'fS': fileSize, 'fC': fileCount, 'dF': deletedFile, 'dD': deletedDirs, 'types': fileType}
		table = render_to_string('dropcloud/dropMetaTable.html',data)	
		dajax.assign("#analysisRes", "innerHTML", table)
	except (Exception, dropbox.rest.ErrorResponse) as e:
		dajax.assign("#statusMeta","innerHTML", str(e))

	return dajax.json()

@dajaxice_register
def searchMetaData(request, form, tokenID):
	""" Search files over meta data """
	
	checkUserAuthentication(request)

	dajax = Dajax()
	desForm = DropMetaSearch(deserialize_form(form))

	if desForm.is_valid():
		try:
			# get metadata and decode it
			token = DropboxToken.objects.get(id=tokenID)
			getMetaInfo = DropboxFileMetadata.objects.filter(tokenID=token).latest('metaTime')
			metaInfo = pickle.loads(base64.b64decode(getMetaInfo.metadata))
			res = list()
			t = int(desForm.cleaned_data['resType'][0])

			for folder in metaInfo:
				for cnt in folder['contents']:
					#deleted 
					if t == 0:
						try:
							if cnt['is_deleted']:
								res.append(cnt)
						except KeyError as e:
							None
					#MIME Type
					elif t == 1:
						if not cnt['is_dir'] and cnt['mime_type'] == desForm.cleaned_data['mimeType']:
							res.append(cnt)
					# All
					elif t == 2:
						res.append(cnt)
						
			table = render_to_string("dropcloud/dropSearchTable.html", {'res': res})
			dajax.assign("#searchRes","innerHTML", table)
		except DropboxFileMetadata.DoesNotExist, DropboxToken.DoesNotExist:
			dajax.assign("#resStatus","innerHTML", "There is a problem with your search :(")
	
	else:
		dajax.assign("#resStatus","innerHTML", "Please fill in all fields")

	return dajax.json()


@dajaxice_register
def getDownloadList(request, tokenID):
	""" Get the list of file to download """
	
	checkUserAuthentication(request)

	dajax = Dajax()

	try:
		tkn = DropboxToken.objects.get(id=tokenID)
		getMetaInfo = DropboxFileMetadata.objects.filter(tokenID=tkn).latest('metaTime')
		metaInfo = pickle.loads(base64.b64decode(getMetaInfo.metadata))
		res = list()
		size = 0

		for f in metaInfo:
			for cnt in f['contents']:
				if not cnt['is_dir'] and "is_deleted" not in cnt:
					res.append(cnt['path'])
					size += float(cnt['bytes'])

		convertSize = size/(1024*1024)
		table = render_to_string("dropcloud/dropDownTable.html", {'res': res, 'convertSize': convertSize})
		dajax.assign("#downList", "innerHTML", table)
	except DropboxToken.DoesNotExist:
		None

	return dajax.json()


@dajaxice_register
def downloadFile(request, fileName, tokenID):
	""" Download a file from the dropbox folder """

	checkUserAuthentication(request)

	dajax = Dajax()

	try:
		tkn = DropboxToken.objects.get(id=tokenID)
		client = dropbox.client.DropboxClient(tkn.accessToken)
		f = client.get_file(fileName)
		downFullPath = os.path.join(settings.DOWNLOAD_DIR, getImportNameFromToken(tkn),"dropbox_"+tkn.userID, os.path.basename(fileName))
		out = open(downFullPath, "wb+")
		out.write(f.read())
		out.close()
		dajax.assign("#fileDownStatus", "innerHTML", "correct")
	except (dropbox.rest.ErrorResponse, Exception) as e:
		dajax.assign("#fileDownStatus","innerHTML", "<p>" + fileName + " download failed</p>")

	return dajax.json()

@dajaxice_register
def downloadWrapper(request, tokenID):
	""" Wrapper for downloader """


	checkUserAuthentication(request)

	dajax = Dajax()

	#check if a directory for this report and dropbox id already exists
	tkn = DropboxToken.objects.get(id=tokenID)
	downReportPath = os.path.join(settings.DOWNLOAD_DIR,getImportNameFromToken(tkn))
	downFullPath = os.path.join(downReportPath,"dropbox_" + tkn.userID)
	
	if not os.path.isdir(downReportPath):
		# create folder
		os.mkdir(downReportPath)

		# folder of dropbox userid
		if not os.path.isdir(downFullPath):
			# create folder
			os.mkdir(downFullPath)

	dajax.assign("#wrapperStatus", "innerHTML", "true")

	return dajax.json()

@dajaxice_register
def comparator(request, tokenID):

	checkUserAuthentication(request)

	dajax = Dajax()

	tkn = DropboxToken.objects.get(id=tokenID)

	#get dropbox metadata
	dropMeta = DropboxFileMetadata.objects.filter(tokenID=tokenID).latest("metaTime")
	cleanedMeta = pickle.loads(base64.b64decode(dropMeta.metadata))
	fileFromMeta = list()

	for meta in cleanedMeta:
		for f in meta['contents']:
			if not f['is_dir']:
				fileFromMeta.append({"file": os.path.basename(f['path']), "hash": None, "localFile": None, "downloaded": False, "full": False, "notinreport": True, "diff": False})

	#get import
	importName = getImportNameFromToken(tkn)
	downReportPath = os.path.join(settings.DOWNLOAD_DIR,importName)
	downFullPath = os.path.join(downReportPath,"dropbox_" + tkn.userID)

	# now check the download directory for the file and compute their hash
	for count in range(0,len(fileFromMeta)):
		thisF = fileFromMeta[count]
		fPath = os.path.join(downFullPath,thisF['file']) 
		if os.path.isfile(fPath):
			# compute hash if file found
			h = crypto.sha256File(fPath)
			thisF['hash'] = h
			thisF['downloaded'] = True

	 # get file of dropbox from report
	uploadDir = os.path.join(settings.UPLOAD_DIR,importName, importName + ".report" )
	jsonReport = json.load(open(uploadDir, "rb"))

	# build list of file cloud from report
	reportList = list()
	for cloud in jsonReport[2]['objects']:
		if cloud['cloudService'].startswith("Dropbox") and cloud['files'] is not None:
			reportList = cloud['files']


	# compare meta and report list and diff
	for count in range(0, len(fileFromMeta)):
		actualMeta = fileFromMeta[count]

		#check if this file is in the report
		for r in reportList:

			# same hash, the file is the same
			if actualMeta['hash'] == r['hash']:
				actualMeta["localFile"] = r
				actualMeta["full"] = True
				actualMeta["notinreport"] = False
				break
			# same file name, propose diff
			elif actualMeta['file'] == os.path.basename(r["path"]):
				actualMets["diff"] = True
				actualMeta["notinreport"] = False
				break
			
	table = render_to_string("dropcloud/dropCompareTable.html",{'hList': fileFromMeta})
	dajax.assign("#hashTable", "innerHTML", table)
	return dajax.json()

@dajaxice_register
def fileRevisioner(request, fileName, tokenID):
	""" Show the list of revision for the file """

	checkUserAuthentication(request)

	dajax = Dajax()
	tkn = DropboxToken.objects.get(id=tokenID)
	client = dropbox.client.DropboxClient(tkn.accessToken)
	fileHistory = client.revisions(fileName)
	table = render_to_string("dropcloud/dropRevisioner.html", {"revisions": fileHistory})
	dajax.assign("#fileRevisionContainer", "innerHTML", table)

	return dajax.json();

def recurseDropTree(folderMetadata, client, depth):
	""" Recurse in each folder """
	res = list()
	
	if folderMetadata['is_dir'] and depth > 0:

		res.append(folderMetadata)

		#get content
		for c in folderMetadata['contents']:
			if c['is_dir']:
				metadata = client.metadata(c['path'])
				# go down one level in the tree
				myres = recurseDropTree(metadata, client, depth-1)
				res += myres
				
		return res

	elif folderMetadata['is_dir'] and depth == 0:
		res.append(folderMetadata)
		return res

def parseDropTree(contList):
	""" Parse the list of file metadata """

	dirCount = len(contList)
	fileSize = 0
	fileCount = 0
	fileType = dict()
	deletedFile = 0
	deletedDirs = 0

	for c in contList:
		for dirCont in c['contents']:
			if not dirCont['is_dir']:
				fileCount += 1
				fileSize += float(dirCont['bytes'])

				key = dirCont['mime_type']
				fileType.setdefault(key, 0)
				fileType[key] += 1

				try:
					if dirCont['is_deleted']:
						deletedFile += 1
				except KeyError as e:
					None
			elif dirCont['is_dir']:
				try:
					if dirCont['is_deleted']:
						deletedDirs += 1
				except KeyError as e:
					None

	fileSize = fileSize/(1024*1024)
	return dirCount, fileSize, fileCount, fileType, deletedFile, deletedDirs

def getImportNameFromToken(token):
	""" Get the import name without extension """
	upload = Upload.objects.get(id=token.importID.id)
	importName = upload.fileName[:-8]
	return importName

def checkUserAuthentication(request):
	""" Check if the user is authenticated """
	if not request.user.is_authenticated():
		sys.exit("Auth required")
