import json,base64,time,os
from downloader.models import FileMetadata,FileDownload,FileHistory
from dashboard.models import MimeType
from webapp.func import dropboxAlternateName
from abstractTimeMaker import AbstractTimeMaker
from cloudservice.drop import DropboxAnalyzer

class DropboxTimeMaker(AbstractTimeMaker):

	def __init__(self,token):
		AbstractTimeMaker.__init__(self,token)

	def constructTimeLineItem(self,item,isHistory = False):

		trashed = False
		date = item['modified']
		parsedDate = list(time.strptime(date,"%a, %d %b %Y %H:%M:%S +0000"))[:6]
		isDir = False
		title = os.path.basename(item['path'])

		#subtract -1 from the month
		parsedDate[1] = parsedDate[1] - 1
		parsedDateStr = ",".join(map(str,parsedDate))

		if isHistory:
			altName = item['rev']
		else:
			altName = dropboxAlternateName(item['path'],date)

		if 'is_deleted'	in item:
			trashed = True

		if item['is_dir']:
			isDir = True

		jStr = '{"timeStr":"'+date+'"}'
		return {'title': title,'isDir': str(isDir),'altName':altName,'trashed':str(trashed),'time': parsedDateStr,'params': jStr}
			
	def formTimeLine(self,resType,mimeType,startDate,endDate):

		d = DropboxAnalyzer(self.t)
		retval = d.metadataSearch(resType,mimeType,startDate,endDate)
		
		buildItem = list()

		for f in retval:
			buildItem.append(self.constructTimeLineItem(f))

		return buildItem

	def filehistoryTimeLine(self,altName):

		#get the filedownload
		fileDownloadObj = self.db.getFileDownload(self.t,altName)

		retval = list()

		#add original file
		for f in self.db.getMetadataParsed(self.t):
			for c in f['contents']:
				if not c['is_dir']:
					if os.path.basename(c['path']) == fileDownloadObj.fileName:
						if 'is_deleted' in c:
							deleted = True
						else: 
							deleted = False

						retval.append(self.constructTimeLineItem(c,deleted))

		for h in self.db.getHistoryForFile(fileDownloadObj):
			hMeta = json.loads(base64.b64decode(h.revisionMetadata))
			retval.append(self.constructTimeLineItem(hMeta,True))

		return retval
