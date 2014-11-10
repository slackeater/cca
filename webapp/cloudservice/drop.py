from importer.models import Upload
import md5, json, base64, dropbox
from dashboard.models import AccessToken, AccountInfo, FileMetadata, MimeType
from django.template.loader import render_to_string

def sessionName(tokenID):
	""" Get the session name """
	return md5.new(str(tokenID)).hexdigest()
	

def userInformation(request, tokenID):
	""" Get the user information """
	obj, created = AccountInfo.objects.get_or_create(tokenID=AccessToken(id=tokenID))

	if created == True:
		c = dropbox.client.DropboxClient(request.session[sessionName(tokenID)])
		userInfo = json.dumps(c.account_info())
		obj.accountInfo = base64.b64encode(userInfo)
		obj.save()
	elif created == False:
		userInfo = json.loads(base64.b64decode(obj.accountInfo))
	
	return render_to_string("dashboard/cloudservice/dropboxUserInfoTable.html",{"accountInfo":userInfo})

def metadataAnalysis(request,update,tokenID):
	""" Dropbox metadata analysis """


	#check if we already have the data
	obj, created = FileMetadata.objects.get_or_create(tokenID=AccessToken.objects.get(id=tokenID))
	c = dropbox.client.DropboxClient(request.session[sessionName(tokenID)])
	
	data = c.metadata("/",include_deleted=True,include_media_info=True)
	diff = False
	metaInfo = list()

	# if is newly created or we want to update
	if created == True or update == 1:
		if update == 1:
			metaDecoded = json.loads(base64.b64decode(obj.metadata))
			if metaDecoded[0]['hash'] != data['hash']:
				diff = True
				 

		#get list of directory if new or update available
		if created or diff:
			metaInfo = recurseDropTree(data, c, 5)
			obj.metadata = base64.b64encode(json.dumps(metaInfo))
			obj.save()
		#no update available
		elif not diff: 
			metaInfo= json.loads(base64.b64decode(obj.metadata))
	# get from db
	else:
		metaInfo= json.loads(base64.b64decode(obj.metadata))

	dirCount, fileSize, fileCount, fileType, deletedFile, deletedDirs = parseDropTree(metaInfo)	
	return render_to_string("dashboard/cloudservice/metaAnalysis.html",{'dropbox': True, 'fC':fileCount,'dC': dirCount,'fS':fileSize,'dF':deletedFile,'dD':deletedDirs,'types':fileType})

def metadataSearch(tokenID, resType, selectedMimeType):
	""" Search over metadata """

	#get meta data
	meta = json.loads(base64.b64decode(FileMetadata.objects.get(tokenID=AccessToken.objects.get(id=tokenID)).metadata))
	res = list()

	for folder in meta:
		for cnt in folder['contents']:
			fID = {'fileID':md5.new(cnt['path']).hexdigest()}
			cnt.update(fID)
			#deleted 
			if resType == 0:
				deleted = cnt.get("is_deleted",False)
				
				if deleted:
					res.append(cnt)
			#mime
			elif resType == 1:
				if not cnt['is_dir'] and cnt['mime_type'] == MimeType.objects.get(id=selectedMimeType).mime:
					res.append(cnt)
			#all
			elif resType == 2:
				res.append(cnt)

	table = render_to_string("dashboard/cloudservice/dropboxSearchTable.html",{'res': res, 'platform': 'dropbox'})
	return table

def fileInfo(tokenID, fileID):
	""" Get the file information """

	#get metadata
	meta = json.loads(base64.b64decode(FileMetadata.objects.get(tokenID=AccessToken.objects.get(id=tokenID)).metadata))
	i = None

	for folder in meta:
		for cnt in folder['contents']:
			if md5.new(cnt['path']).hexdigest() == fileID:
				i = cnt
				break;
	
	table = render_to_string("dashboard/cloudservice/dropboxFileInfoTable.html",{'item':i,'platform':'dropbox'})
	return table

def fileHistory(id,sessionCredentials):
	""" Get file history """

	client = dropbox.client.DropboxClient(sessionCredentials)
	fileHistory = client.revisions(id)
	table = render_to_string("dashboard/cloudservice/dropboxRevisioner.html",{"revisions": fileHistory})
	return table

def downloadSize(tokenID):
	""" Compute the size of the download """

	meta = json.loads(base64.b64decode(FileMetadata.objects.get(tokenID=AccessToken.objects.get(id=tokenID)).metadata))
	size = 0	
	fileCount = 0 

	for folder in meta:
		for cnt in folder['contents']:
			if not cnt['is_dir'] and 'is_deleted' not in cnt:
				size += float(cnt['bytes'])
				fileCount += 1

	size = size/(1024*1024)
	table = render_to_string("dashboard/cloudservice/downloadSize.html", {'platform': platform, 'size': size,'count': fileCount})
	return table
	

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
