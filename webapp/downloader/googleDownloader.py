from models import AccessToken,FileDownload,FileMetadata,FileHistory
## OAuth Stuff

def serviceBuilder(serviceName, version, httpObj):
	""" Create a service used to perform future API calls """
	return build(serviceName, version, httpObj)

def httpCreator(credentials):
	""" Create an HTTP object to be passed to a build service """

	http = httplib2.Http()

	#get credentials 
	credentials = OAuth2Credentials.from_json(credentials)

	return credentials.authorize(http)


def driveService(credentials)
	""" A Google Drive Service """
	h = httpCreator(credential)
	return serviceBuilder("drive","v2",h)


def downloadMetaData(tokenID):
	pass	
