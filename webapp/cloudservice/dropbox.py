from dashboard.models import DropboxToken
from importer.models import Upload

def retrieveCredentials(request, importIDget, tokenID, sessionName):
	""" Retrieve the credentials from the DB """

	sessionCred = request.session.get(sessionName, "none")

	#check if a session credentials has been already created
	if sessionCred != "none":
		return None

	if importIDget != 0 and tokenID != 0:
		try:
			token = DropboxToken.objects.get(importID=Upload.objects.get(importID=Upload.objects.get(id=importIDget), id=tokenID))

			# create credentials
			request.session[sessionName] = token.accessToken
		except DropboxToken.DoesNotExist:
			raise Exception("Invalid Parameters")


def userInformation(request, sessionName, tokenID):
	""" Get the user information """


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
