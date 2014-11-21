import json,base64,time,os
from downloader.models import FileMetadata,FileDownload,FileHistory
from dashboard.models import MimeType
from webapp.func import dropboxAlternateName

def constructLineItem(item):

	trashed = False
	date = item['modified']
	parsedDate = list(time.strptime(date,"%a, %d %b %Y %H:%M:%S +0000"))[:6]
	#subtract -1 from the month
	parsedDate[1] = parsedDate[1] - 1
	parsedDateStr = ",".join(map(str,parsedDate))

	if 'is_deleted'	in item:
		trashed = True

	jStr = '{"timeStr":"'+date+'","altName":"'+dropboxAlternateName(item['path'],date)+'","trashed":"'+str(trashed)+'"}'
	return {'title': os.path.basename(item['path']),'time': parsedDateStr,'params': jStr}
	
def formTimeline(cloudItem,token,resType,mimeType):

	retval = list()

	meta = json.loads(base64.b64decode(FileMetadata.objects.get(tokenID=token).metadata))

	for f in meta:
		for c in f['contents']:
			if not c['is_dir']: 
				if resType == 0:
					if 'is_deleted' in c:
						retval.append(constructLineItem(c))
				elif resType == 1:
					mime = MimeType.objects.get(id=mimeType).mime
					
					if c['mime_type'] == mime:
						retval.append(constructLineItem(c))
				elif resType == 2:
					retval.append(constructLineItem(c))

	return retval

def filehistoryTimeline(cloudItem,token,altName):

	#get the filedownload
	fileDownloadObj = FileDownload.objects.get(alternateName=altName,tokenID=token)
	retval = list()

	#get history for this file
	history = FileHistory.objects.filter(fileDownloadID=fileDownloadObj)

	for h in history:
		hMeta = json.loads(base64.b64decode(h.revisionMetadata))
		retval.append(constructLineItem(hMeta))

	return retval
