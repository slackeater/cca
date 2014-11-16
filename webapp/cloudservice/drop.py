from importer.models import Upload
import md5, json, base64, dropbox
from dashboard.models import MimeType
from downloader.models import AccessToken,FileMetadata,FileHistory,FileHistory
from django.template.loader import render_to_string
from webapp.func import dropboxAlternateName

def metadataAnalysis(request,tokenID):
	""" Dropbox metadata analysis """

	fm = FileMetadata.objects.get(tokenID=AccessToken.objects.get(id=tokenID))
	metaInfo= json.loads(base64.b64decode(fm.metadata))

	dirCount, fileSize, fileCount, fileType, deletedFile, deletedDirs = parseDropTree(metaInfo)	
	return render_to_string("dashboard/cloudservice/metaAnalysis.html",{'dropbox': True, 'fC':fileCount,'dC': dirCount,'fS':fileSize,'dF':deletedFile,'dD':deletedDirs,'types':fileType})

def metadataSearch(tokenID, resType, selectedMimeType):
	""" Search over metadata """

	#get meta data
	meta = json.loads(base64.b64decode(FileMetadata.objects.get(tokenID=AccessToken.objects.get(id=tokenID)).metadata))
	res = list()

	for folder in meta:
		for cnt in folder['contents']:
			fID = {'fileID':dropboxAlternateName(cnt['path'],cnt['modified'])}
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
			altName = dropboxAlternateName(cnt['path'],cnt['modified'])
			if  altName == fileID:
				i = cnt
				i['fileID'] = altName
				break;
	
	table = render_to_string("dashboard/cloudservice/dropboxFileInfoTable.html",{'item':i,'platform':'dropbox'})
	return table

def fileHistory(fileDB):
	""" Get file history """

	#get all revision
	revDB = FileHistory.objects.filter(fileDownloadID=fileDB)
	revisions = list()	

	for r in revDB:
		decR = json.loads(base64.b64decode(r.revisionMetadata))
		revisions.append(decR)

	table = render_to_string("dashboard/cloudservice/dropboxRevisioner.html",{"revisions": revisions})
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
