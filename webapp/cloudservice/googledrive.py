from importer.models import Upload
from oauth2client.client import OAuth2Credentials
import base64, sys, httplib2, json
from apiclient.discovery import build
from dashboard.models import MimeType
from downloader.models import AccessToken,FileMetadata,FileHistory
from django.template.loader import render_to_string
from django.utils import timezone
from django.conf import settings
import md5, os

## Functions
def getMetaData(tokenID):
	""" Get the metadata for a given token ID """
	token = AccessToken.objects.get(id=tokenID)
	meta = json.loads(base64.b64decode(FileMetadata.objects.get(tokenID=token).metadata))
	return meta

def metadataAnalysis(request, tokenID):
	""" Analyse metadata """
	
	fm = FileMetadata.objects.get(tokenID=AccessToken.objects.get(id=tokenID))
	files = json.loads(base64.b64decode(fm.metadata))
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

def fileHistory(downFile):
	""" Get the file history """

	#get all history for the file with that id
	allRev = FileHistory.objects.filter(fileDownloadID=downFile)
	revisions = list()

	for r in allRev:
		decR = json.loads(base64.b64decode(r.revisionMetadata))
		revisions.append(decR)

	table = render_to_string("dashboard/cloudservice/googleRevisionTable.html", {'rev': revisions})
	return table
	
def comparator():
	""" compare files """
	#TODO
