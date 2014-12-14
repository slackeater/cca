from importer.models import Upload
from oauth2client.client import OAuth2Credentials
import base64, sys, httplib2, json
from apiclient.discovery import build
from dashboard.models import MimeType
from downloader.models import AccessToken,FileMetadata,FileHistory
from django.template.loader import render_to_string
from django.conf import settings
import md5, os
from webapp import databaseInterface
from abstractAnalyzer import AbstractAnalyzer
import math

class GoogleAnalyzer(AbstractAnalyzer):

	def __init__(self,token):
		AbstractAnalyzer.__init__(self,token)

	def metadataAnalysis(self):
		""" Analyse metadata """
		
		stat = self.getFileStats(self.metadata)
		parsedTable = render_to_string("dashboard/cloudservice/googleMetaAnalysis.html",{'stat':stat})
		return parsedTable

	def getFileStats(self,files):
		""" Get statistics about file on google drive and documents """

		deletedCount = 0
		driveFiles = 0
		docsFiles = 0
		driveFileSize = 0
		mimeType = dict()

		for item in files:

			if item['labels']['trashed']:
				deletedCount += 1	

			if 'fileSize' in item:
				driveFiles += 1
				driveFileSize += float(item['fileSize'])
			else:
				docsFiles += 1

			mimeType.setdefault(item['mimeType'],0)
			mimeType[item['mimeType']] += 1

		#dictionary with stats
		stat = dict()
		stat['dC'] = deletedCount
		stat['driveF'] = driveFiles
		stat['docsF'] = docsFiles
		stat['driveFS'] = driveFileSize/math.pow(2,20)
		stat['mime'] = mimeType
		
		return stat

	def metadataSearch(self, searchType,mimeType,startDate,endDate):
		""" Search through metadata """

		searchItem = list()

		# all
		if searchType == 2:
			searchItem = self.metadata
		else:
			for i in self.metadata:
				#deleted
				if searchType == 0:
					if i['labels']['trashed']:
						searchItem.append(i)
				# mimetype
				elif searchType == 1:
					m = MimeType.objects.get(id=mimeType)
					if i['mimeType'] == m.mime:
						searchItem.append(i)

		return searchItem

	def textualMetadataSearch(self,searchType,mimeType,startDate,endDate):
		searchItem = self.metadataSearch(searchType,mimeType,startDate,endDate)
		table = render_to_string("dashboard/cloudservice/googleSearchTable.html", {'data': searchItem,'platform':'google'})
		return table

	def fileInfo(self, fileID):
		""" Get information of a file """
		
		i = None

		for item in self.metadata:
			if fileID == item['id']:
				i = item
				break;
		
		table = render_to_string("dashboard/cloudservice/googleFileInfoTable.html",{'item': i,'platform':'google'})
		return table

	def fileHistory(self,fileId):
		""" Get the file history """

		#get all history for the file with that id
		revisions = list()

		fileObject = self.db.getFileDownload(self.t,fileId)

		for r in self.db.getHistoryForFile(fileObject):
			decR = json.loads(base64.b64decode(r.revisionMetadata))
			revisions.append(decR)

		table = render_to_string("dashboard/cloudservice/googleRevisionTable.html", {'rev': revisions})
		return table
