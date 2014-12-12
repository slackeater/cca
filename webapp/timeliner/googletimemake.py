from clouditem.models import CloudItem
from importer.models import Upload
from downloader.models import FileMetadata,FileHistory,FileDownload
from dashboard.models import MimeType
from django.conf import settings
import os,json,sqlite3,time
from urlparse import urlparse
from datetime import datetime,timedelta
import pytz, base64, strict_rfc3339
from abstractTimeMaker import AbstractTimeMaker
from cloudservice.googledrive import GoogleAnalyzer

class GoogleTimeMaker(AbstractTimeMaker):

	def __init__(self,token):
		AbstractTimeMaker.__init__(self,token)
		
	def constructTimeLineItem(self,item,isHistory = False):
		""" Construct an element to be added to the timeline """

		if isHistory:
			displayDate = item['modifiedDate']

			if "lastModifyingUserName" in item:
				title = item['lastModifyingUserName']
			else:
				title = item['id']

			trashed = str(False)
		else:
			displayDate = item['createdDate']
			title = item['title']
			trashed = str(item['labels']['trashed'])

		isDir = False
		altName = item['id']

		if item['mimeType'] == "application/vnd.google-apps.folder":
			isDir = True
			altName = ""

		# date
		dateTuple = list(time.gmtime(strict_rfc3339.rfc3339_to_timestamp(displayDate)))[:6]
		#month -1 because javascript Date goes from 0-11
		dateTuple[1] = dateTuple[1] - 1
		date = ",".join(map(str,dateTuple))

		jStr = '{"timeStr":"'+displayDate+'"}'
		return {'title': title,'time':date,'isDir':str(isDir),'trashed':trashed,'altName': altName,'params':jStr}

	def formTimeLine(self,resType,mimeType,startDate,endDate):
		
		ga = GoogleAnalyzer(self.t)
		retval = ga.metadataSearch(resType,mimeType,startDate,endDate)
		
		buildList = list()

		for r in retval:
			buildList.append(self.constructTimeLineItem(r))

		return buildList

	def filehistoryTimeLine(self,altName):

		fileDownloadObj = self.db.getFileDownload(self.t,altName)
		retval = list()	

		#get all history for this file
		for h in self.db.getHistoryForFile(fileDownloadObj):
			hMeta = json.loads(base64.b64decode(h.revisionMetadata))
			retval.append(self.constructTimeLineItem(hMeta,True))

		return retval
