from dashboard.models import AccessToken 
from importer.models import Upload
from oauth2client.client import OAuth2Credentials
import base64, sys, httplib2, json
from apiclient.discovery import build
from dashboard.models import AccountInfo, FileMetadata, MimeType
from django.template.loader import render_to_string
from django.utils import timezone
from django.conf import settings
import md5, os
## OAuth Stuff

def serviceBuilder(serviceName, version, httpObj):
	""" Create a service used to perform future API calls """
	return build(serviceName, version, httpObj)

def httpCreator(credentialSession):
	""" Create an HTTP object to be passed to a build service """

	http = httplib2.Http()
	
	#get credentials 
	credentials = OAuth2Credentials.from_json(credentialSession)

	return credentials.authorize(http)

## Functions
def getMetaData(tokenID):
	""" Get the metadata for a given token ID """
	token = AccessToken.objects.get(id=tokenID)
	meta = json.loads(base64.b64decode(FileMetadata.objects.get(tokenID=token).metadata))
	return meta

def userInformation(request, tokenID):
	""" Save and display userinformation  """

	sessionName = md5.new(str(tokenID)).hexdigest()

	#insert into database if not present
	obj, created = AccountInfo.objects.get_or_create(tokenID=AccessToken(id=tokenID))
	
	if created == True:
		httpObj = httpCreator(request.session[sessionName])
		user_info_service = serviceBuilder("oauth2","v2",httpObj)
		info = user_info_service.userinfo().get().execute()
					
		#update the object
		userInfo = info
		obj.accountInfo = base64.b64encode(json.dumps(info))
		obj.save()
	# userinfo already present
	elif created == False:
		userInfo = json.loads(base64.b64decode(obj.accountInfo))

	#get e-mail and e-mail verified from credentials in session
	credJson = json.loads(request.session[sessionName])
	emailVerified = credJson['token_response']['id_token']['email_verified']
	email = credJson['token_response']['id_token']['email']

	return render_to_string("dashboard/cloudservice/googleUserInfoTable.html", {'accountInfo': userInfo, 'email': email,  'emailVerified': emailVerified})

def metadataAnalysis(request, update, tokenID):
	""" Analyse metadata """
	
	sessionName = md5.new(str(tokenID)).hexdigest()

	#build the drive service
	drive_service = serviceBuilder("drive","v2",httpCreator(request.session[sessionName]))
	
	obj, created = FileMetadata.objects.get_or_create(tokenID=AccessToken.objects.get(id=tokenID))
	files = None
	#build the drive service
	drive_service = serviceBuilder("drive","v2",httpCreator(request.session[sessionName]))
	
	if created or update == 1:
		files = drive_service.files().list().execute()
		filesDB = base64.b64encode(json.dumps(files))
		obj.metadata = filesDB
		obj.metaTime = timezone.now()
		obj.save()
	else: #get from db
		files = json.loads(base64.b64decode(obj.metadata))

	stat = getFileStats(files)
	return render_to_string("dashboard/cloudservice/metaAnalysis.html", {'stat': stat,'google': True})

def getFileStats(files):
	""" Get statistics about file on google drive and documents """

	deletedCount = 0
	driveFiles = 0
	docsFiles = 0
	driveFileSize = 0
	mimeType = dict()

	for item in files["items"]:

		if item['labels']['trashed']:
			deletedCount += 1	

		if 'fileSize' in item:
			driveFiles += 1
			driveFileSize += float(item['fileSize'])
		else:
			docsFiles += 1

		mimeType.setdefault(item['mimeType'],0)
		mimeType[item['mimeType']] += 1
	
	stat = dict()
	stat['dC'] = deletedCount
	stat['driveF'] = driveFiles
	stat['docsF'] = docsFiles
	stat['driveFS'] = driveFileSize
	stat['mime'] = mimeType
	
	return stat

def metadataSearch(tokenID, resType, selectedMimeType):
	""" Search through metadata """

	gMetaInfo = getMetaData(tokenID)	
	
	searchItem = list()

	# all
	if resType == 2:
		searchItem = gMetaInfo['items']
	else:
		for i in gMetaInfo['items']:
			#deleted
			if resType == 0:
				if i['labels']['trashed']:
					searchItem.append(i)
			# mimetype
			elif resType == 1:
				m = MimeType.objects.get(id=selectedMimeType)
				if i['mimeType'] == m.mime:
					searchItem.append(i)

	table = render_to_string("dashboard/cloudservice/googleSearchTable.html", {'data': searchItem,'platform':'google'})
	return table	

def fileInfo(tokenID, fileID):
	""" Get information of a file """
	
	gMetaInfo = getMetaData(tokenID)
	i = None

	for item in gMetaInfo['items']:
		if fileID == item['id']:
			i = item
			break;
	
	table = render_to_string("dashboard/cloudservice/googleFileInfoTable.html",{'item': i,'platform':'google'})
	return table

def fileHistory(fileID, sessionData):
	""" Get the file history """
	drive_service = serviceBuilder("drive", "v2",httpCreator(sessionData))
	
	#get the revisions
	revisions = drive_service.revisions().list(fileId=fileID).execute().get('items',[])

	table = render_to_string("dashboard/cloudservice/googleRevisionTable.html", {'rev': revisions})
	return table
	
def downloadSize(tokenID):
	""" Download files """

	metadata = getMetaData(tokenID)
	fileSize = 0
	count = 0
	fileListID = list()

	for item in metadata['items']:
		if 'fileSize' in item:
			fileSize += float(item['fileSize'])
			count += 1
			fileListID.append(item['id'])


	fileSize = fileSize/(1024*1024)

	if fileSize <= 500:
		downloader = render_to_string("dashboard/cloudservice/foregroundDownload.html",{'res':fileListID})
	else:
		downloader = None

	table = render_to_string("dashboard/cloudservice/downloadSize.html",{'platform': 'google','size': fileSize,'count':count,'downloader': downloader})
	return table

def downloadFile(fileID,sessionData,tokenID):
	""" Download a single file """

	#get download url
	metaData = getMetaData(tokenID)
	sName = md5.new(str(tokenID)).hexdigest()
	downURL = None
	fName = None

	for m in metaData['items']:
		if fileID == m['id']:
			downURL = m['downloadUrl']
			fName = m['title']
			break
	
	downloadDir = os.path.join(settings.DOWNLOAD_DIR,sName)

	if os.path.isdir(downloadDir):
		if downURL:
			s = serviceBuilder("drive","v2",httpCreator(sessionData))
			resp, content = s._http.request(downURL)
			
			if resp.status == 200:
				return True, fName
			else:
				return False, resp.status
	
	return False, None

def comparator():
	""" compare files """
	#TODO
