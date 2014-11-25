from clouditem.models import CloudItem
from importer.models import Upload
from downloader.models import FileMetadata,FileHistory,FileDownload
from dashboard.models import MimeType
from django.conf import settings
import os,json,sqlite3,time
from urlparse import urlparse
from datetime import datetime,timedelta
import pytz, base64, strict_rfc3339

def constructLineItem(item,isHistory = False):
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

	jStr = '{"timeStr":"'+displayDate+'","altName":"'+altName+'","trashed":"'+trashed+'"}'
	return {'title': title,'time':date,'isDir':str(isDir),'params':jStr}

def decodeTransition(trans):
	""" Return the type of transition """

	mask = 0xff

	res = trans & mask

	if res == 0:
		return "LINK"
	elif res == 1:
		return "TYPED"
	elif res == 2:
		return "AUTO_BOOKMARK"
	elif res == 3:
		return "AUTO_SUBFRAME"
	elif res == 4:
		return "MANUAL_SUBFRAME"
	elif res == 5:
		return "GENERATED"
	elif res == 6:
		return "START_PAGE"
	elif res == 7:
		return "FORM_SUBMIT"
	elif res == 8:
		return "RELOAD"
	elif res == 9:
		return "KEYWORD"
	elif res == 10:
		return "KEYWORD_GENERATED"

def docmentsHistoryTimeline(cloudItem,token):
	""" Generate a list of browse history """
	
	retval = list()
	
	#get the report
	rep = Upload.objects.get(cloudItemID=cloudItem)

	#report path
	fullReportPath = os.path.join(settings.UPLOAD_DIR,rep.fileName)

	#read report for profile
	with open(os.path.join(fullReportPath,rep.fileName+".report"),"rb") as r:
		jsonReport = json.load(r)
		browser = jsonReport[1]
		folder = None

		for b in browser['objects']:
			if "Google Chrome" in b['name']:
				folder = "chrome-copy"

				for p in b['profiles']:

					for f in p['fileListHashes']:
						
						if "History" in f['path']:
							historyFile = os.path.join(fullReportPath,folder,p['profileName'],"History")
							# connect to db
							conn = sqlite3.connect(historyFile)

							for row in conn.execute("SELECT urls.url, urls.title, urls.visit_count, urls.typed_count, urls.last_visit_time, urls.hidden, visits.visit_time, visits.from_visit, visits.transition FROM urls, visits WHERE urls.id =visits.url"):
								parsed_uri = urlparse(row[0])
								domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)

								epoch = datetime(1601, 1, 1, tzinfo=pytz.UTC)
								cookie_microseconds_since_epoch = row[4]
								cookie_datetime = epoch + timedelta(microseconds=cookie_microseconds_since_epoch)
								print "TS"
								ts = time.mktime(cookie_datetime.timetuple())
								print ts
								myTime = time.gmtime(ts)
								tStr = str(myTime.tm_year) + "," + str(myTime.tm_mon-1) + "," + str(myTime.tm_mday),
								minStr = "0" + str(myTime.tm_min) if myTime.tm_min <= 9 and myTime.tm_min != 0 else str(myTime.tm_min)
								secStr = "0" + str(myTime.tm_sec) if myTime.tm_sec <= 9 and myTime.tm_sec != 0 else str(myTime.tm_sec)
								hours = str(myTime.tm_hour)+":"+minStr+":"+secStr
								
								retval.append({'hour':hours,'site':domain,'trans': decodeTransition(row[8]),'timeYear':myTime.tm_year,"timeMonth":myTime.tm_mon,"timeDay":myTime.tm_mday})

	return retval

def formTimeline(cloudItem,token,resType,mimeType):

	meta = json.loads(base64.b64decode(FileMetadata.objects.get(tokenID=token).metadata))
	retval = list()

	for f in meta['items']:
			
		if resType == 0:
			if f['labels']['trashed']:
				retval.append(constructLineItem(f))
		elif resType == 1:
			#get mimetype
			mime = MimeType.objects.get(id=mimeType).mime

			if f['mimeType'] == mime:
				retval.append(constructLineItem(f))
		elif resType == 2:
			retval.append(constructLineItem(f))

	return retval

def filehistoryTimeline(cloudItem,token,altName):

	fileDownloadObj = FileDownload.objects.get(alternateName=altName,tokenID=token)
	retval = list()	
	#get all history for this file

	print fileDownloadObj.id
	history = FileHistory.objects.filter(fileDownloadID=fileDownloadObj)
	
	for h in history:
		hMeta = json.loads(base64.b64decode(h.revisionMetadata))
		print hMeta['id']
		retval.append(constructLineItem(hMeta,True))

	return retval
