from importer.models import Upload
from oauth2client.client import OAuth2Credentials
import base64, sys, httplib2, json
from apiclient.discovery import build
from dashboard.models import MimeType
from downloader.models import AccessToken,FileMetadata,FileHistory
from django.template.loader import render_to_string
from django.conf import settings
import md5, os,time
from webapp import databaseInterface
from abstractAnalyzer import AbstractAnalyzer
import math,time,strict_rfc3339
from webapp.func import *
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

	def emailSearch(self,email):
		""" Search through email """

		res = list()

		for i in self.metadata:
			if "owners" in i and i['mimeType'] != MimeType.objects.get(id=1340).mime:

				for o in i['owners']:

					if o['emailAddress'] == email:
						print "Appending"
						res.append(i)

				#TODO add history

		return res

	def metadataSearch(self, searchType,mimeType,startDate,endDate):
		""" Search through metadata """

		searchItem = list()

		startDateTs = float(getTimestamp(startDate))
		endDateTs = float(getTimestamp(endDate))

		for i in self.metadata:

			creationTs = strict_rfc3339.rfc3339_to_timestamp(i['createdDate'])
			
			#check start date
			if creationTs >= startDateTs and creationTs <= endDateTs:
					
					#deleted
					if searchType == 0:
						if i['labels']['trashed']:
							searchItem.append(i)
					# mimetype
					elif searchType == 1:
						m = MimeType.objects.get(id=mimeType)
						if i['mimeType'] == m.mime:
							searchItem.append(i)
					#all
					elif searchType == 2:
						searchItem.append(i)
	
		return searchItem

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
