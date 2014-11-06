from dashboard.models import GoogleDriveToken 
from importer.models import Upload
from oauth2client.client import OAuth2Credentials
import base64, sys, httplib2, json
from apiclient.discovery import build
from models import GoogleAccountInfo, GoogleFileMetadata
from django.template.loader import render_to_string
from django.utils import timezone
## OAuth Stuff

def retrieveCredentials(request, importIDget, tokenID, sessioName):
	""" Retrieve the credentials from the db """

	#check if a session with credentials has been already created
	sessionCred = request.session.get(sessioName, "none") 

	if sessionCred != "none":
		#we already have this variable set
		return None

	# we have all the parameters
	if importIDget != 0 and tokenID != 0:
		try:
			token = GoogleDriveToken.objects.get(importID=Upload.objects.get(id=importIDget), id=tokenID)
		
			# create credentials
			request.session[sessioName] = base64.b64decode(token.accessToken)
		except GoogleDriveToken.DoesNotExist:
			raise Exception("Invalid parameters")	

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


def userInformation(request, sessionName, tokenID):
	""" Save and display userinformation  """

	#insert into database if not present
	obj, created = GoogleAccountInfo.objects.get_or_create(tokenID=GoogleDriveToken(id=tokenID))
	
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

	return {'userInfoTable': render_to_string("cloudservice/googleUserInfoTable.html", {'accountInfo': userInfo, 'email': email,  'emailVerified': emailVerified})}

def metadataAnalysis(request, sessionName, update, tokenID):
	""" Analyse metadata """
	
	#build the drive service
	drive_service = serviceBuilder("drive","v2",httpCreator(request.session[sessionName]))
	
	obj, created = GoogleFileMetadata.objects.get_or_create(tokenID=GoogleDriveToken.objects.get(id=tokenID))
	files = None
	#build the drive service
	drive_service = serviceBuilder("drive","v2",httpCreator(request.session[sessionName]))
	
	if created or update:
		files = drive_service.files().list().execute()
		filesDB = base64.b64encode(json.dumps(files))
		obj.metadata = filesDB
		obj.metaTime = timezone.now()
		obj.save()
	else: #get from db
		files = json.loads(base64.b64decode(obj.metadata))

	stat = getFileStats(files)
	return render_to_string("cloudservice/googleMetaAnalysis.html", {'stat': stat})

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

def metadataSearch():
	""" Search through metadata """

def downloader():
	""" Download files """

def comparator():
	""" compare files """
