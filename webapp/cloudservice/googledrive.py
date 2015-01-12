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
from webapp import constConfig

class GoogleAnalyzer(AbstractAnalyzer):
	""" This class represents a Google analyzer """

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

	def metadataSearchType(self,item,searchType,searchEmail,searchFile,searchGivenName):
		
		searchResItem = None

		#e-mail
		if searchType == constConfig.CS_SEARCH_TYPE_EMAIL:
			if "owners" in item and item['mimeType'] != MimeType.objects.get(id=1340).mime:
				for o in item['owners']:
					if o['emailAddress'] == searchEmail:
						searchResItem = item

			#TODO include history??
				
		#filename
		elif searchType == constConfig.CS_SEARCH_TYPE_FILENAME:
			if "title" in item and searchFile in item["title"]:
				searchResItem = item
		#givenname
		elif searchType == constConfig.CS_SEARCH_TYPE_GIVENNAME:
			if ("lastModifyingUserName" in item and searchGivenName in item["lastModifyingUserName"]) or ("ownerName" in item and searchGivenName in item["ownerNames"]):
				searchResItem = item
		#all
		elif searchType == constConfig.CS_SEARCH_TYPE_ALL:
			searchResItem = item
			
		return searchResItem

	def metadataSearchFilters(self,filterType,item,mimeType):
		
		filterRes = None

		#deleted
		if filterType == constConfig.CS_SEARCH_FILTER_DELETED:
			if item['labels']['trashed']:
				filterRes = item
		# mimetype
		elif filterType == constConfig.CS_SEARCH_FILTER_MIME:
			m = MimeType.objects.get(id=mimeType)
			if item['mimeType'] == m.mime:
				filterRes = item
		#all
		elif filterType == constConfig.CS_SEARCH_FILTER_ALL:
			filterRes = item

		return filterRes

	def metadataSearch(self,searchType,searchEmail,searchFile,searchGivenName,filterType,mimeType,startDate,endDate):
		""" Search through metadata """

		searchItem = list()

		startDateTs = float(getTimestamp(startDate))
		endDateTs = float(getTimestamp(endDate))

		for i in self.metadata:
			creationTs = strict_rfc3339.rfc3339_to_timestamp(i['createdDate'])
			
			#check temporal period
			if creationTs >= startDateTs and creationTs <= endDateTs:
					prunedRes = self.metadataSearchType(i,searchType,searchEmail,searchFile,searchGivenName)

					if prunedRes != None:
						#now apply filters
						filteredRes = self.metadataSearchFilters(filterType,prunedRes,mimeType)

						if filteredRes != None:
							searchItem.append(filteredRes)
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
