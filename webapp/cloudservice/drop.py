from importer.models import Upload
import md5, json, base64, dropbox, time
from dashboard.models import MimeType
from downloader.models import AccessToken,FileMetadata,FileHistory,FileHistory
from django.template.loader import render_to_string
from webapp.func import dropboxAlternateName,getTimestamp
from abstractAnalyzer import AbstractAnalyzer
from dateutil import parser
from webapp import constConfig


class DropboxAnalyzer(AbstractAnalyzer):
	""" This class represent a Dropbox analyzer """

	def __init__(self,token):
		AbstractAnalyzer.__init__(self,token)

	def metadataAnalysis(self):
		""" Dropbox metadata analysis """

		stat = self.parseDropTree(self.metadata)	

		return render_to_string("dashboard/cloudservice/metaAnalysis.html",{'dropbox': True, 'stat':stat})

	def medatadaSearchType(self,item,searchType,searchEmail,searchFile,searchGivenName):

		searchResItem = None

		#e-mail
		if searchType == constConfig.CS_SEARCH_TYPE_EMAIL:
			#email search not supported with dropbox
			pass
		#filename
		elif searchType == constConfig.CS_SEARCH_TYPE_FILENAME:
			if searchFile in item['path']:
				searchResItem = item
		#givenname
		elif searchType == constConfig.CS_SEARCH_TYPE_GIVENNAME:
			if "modifier" in item and item['modifier'] is not None and searchGivenName in item['modifier']['display_name']:
				searchResItem = item
		#all
		elif searchType == constConfig.CS_SEARCH_TYPE_ALL:
			searchResItem = item

		return searchResItem

	def metadataSearchFilters(self,filterType,item,mimeType):

		filterRes = None

		#deleted 
		if filterType == constConfig.CS_SEARCH_FILTER_DELETED:
			deleted = item.get("is_deleted",False)
			
			if deleted:
				filterRes = item
		#mime
		elif filterType == constConfig.CS_SEARCH_FILTER_MIME:
			if not item['is_dir'] and item['mime_type'] == MimeType.objects.get(id=mimeType).mime:
				filterRes = item
		#all
		elif filterType == constConfig.CS_SEARCH_FILTER_ALL:
			filterRes = item

		return filterRes

	def metadataSearch(self, searchType,searchEmail,searchFile,searchGivenName,filterType,mimeType,startDate,endDate):
		""" Search over metadata """

		res = list()

		startDateTs = float(getTimestamp(startDate))
		endDateTs = float(getTimestamp(endDate))

		for folder in self.metadata:
			for cnt in folder['contents']:
				
				modifiedTs = float(getTimestamp(parser.parse(cnt['modified'])))

				if modifiedTs >= startDateTs and modifiedTs <= endDateTs:

					fID = {'fileID':dropboxAlternateName(cnt['path'],cnt['modified'])}
					cnt.update(fID)

					prunedRes = self.medatadaSearchType(cnt,searchType,searchEmail,searchFile,searchGivenName)

					if prunedRes != None:
						filterRes = self.metadataSearchFilters(filterType,cnt,mimeType)

						if filterRes != None:
							res.append(filterRes)
				
		return res

	def fileInfo(self, fileID):
		""" Get the file information """

		i = None

		for folder in self.metadata:
			for cnt in folder['contents']:
				altName = dropboxAlternateName(cnt['path'],cnt['modified'])
				if  altName == fileID:
					i = cnt
					i['fileID'] = altName
					break;
		
		table = render_to_string("dashboard/cloudservice/dropboxFileInfoTable.html",{'item':i,'platform':'dropbox'})
		return table

	def fileHistory(self,fileId):
		""" Get file history """

		#get all revision
		fileObject = self.db.getFileDownload(self.t,fileId)
		revisions = list()	

		for r in self.db.getHistoryForFile(fileObject):
			decR = json.loads(base64.b64decode(r.revisionMetadata))
			revisions.append(decR)

		table = render_to_string("dashboard/cloudservice/dropboxRevisioner.html",{"revisions": revisions})
		return table

	def parseDropTree(self,contList):
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
