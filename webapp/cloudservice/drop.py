from importer.models import Upload
import md5, json, base64, dropbox
from dashboard.models import MimeType
from downloader.models import AccessToken,FileMetadata,FileHistory,FileHistory
from django.template.loader import render_to_string
from webapp.func import dropboxAlternateName

def metadataAnalysis(request,token):
	""" Dropbox metadata analysis """

	fm = FileMetadata.objects.get(tokenID=token)
	metaInfo= json.loads(base64.b64decode(fm.metadata))
	stat = parseDropTree(metaInfo)	

	return render_to_string("dashboard/cloudservice/metaAnalysis.html",{'dropbox': True, 'stat':stat})

def metadataSearch(token, resType, selectedMimeType):
	""" Search over metadata """

	#get meta data
	meta = json.loads(base64.b64decode(FileMetadata.objects.get(tokenID=token).metadata))
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

def fileInfo(token, fileID):
	""" Get the file information """

	#get metadata
	meta = json.loads(base64.b64decode(FileMetadata.objects.get(tokenID=token).metadata))
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

	#dictionary with stats
	stat = dict()
	stat['dC'] = dirCount
	stat['fC'] = fileCount
	stat['fS'] = fileSize
	stat['dF'] = deletedFile
	stat['dD'] = deletedDirs
	stat['mime'] = fileType

	return stat
