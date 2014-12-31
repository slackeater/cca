from abstractBrowserFile import AbstractBrowserFile
import os,sqlite3,urlparse,time,pytz
from datetime import datetime,timedelta
class GoogleChromeFiles(AbstractBrowserFile):

	def __init__(self,folderPath,profile):
		self.folderName = os.path.join(folderPath,"chrome-copy",profile)
		print self.folderName
		AbstractBrowserFile.__init__(self)

	def constructTimeLineItem(self):
		return

	def decodeTransition(self,trans):
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

	def generateTimeLine(self,domainFilter):
		""" Generate a list of browse history """
		
		conn = sqlite3.connect(os.path.join(self.folderName,"History"))
		retval = list()

		# history
		for row in conn.execute("SELECT urls.url, urls.title, urls.visit_count, urls.typed_count, urls.last_visit_time, urls.hidden, visits.visit_time, visits.from_visit, visits.transition FROM urls, visits WHERE urls.id =visits.url"):
			if (domainFilter is not None and domainFilter in row[0]) or domainFilter is None:
				parsed_uri = urlparse.urlparse(row[0])
				domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)

				epoch = datetime(1601, 1, 1, tzinfo=pytz.UTC)
				cookie_microseconds_since_epoch = row[4]
				cookie_datetime = epoch + timedelta(microseconds=cookie_microseconds_since_epoch)

				ts = time.mktime(cookie_datetime.timetuple())

				myTime = time.gmtime(ts)
				tStr = str(myTime.tm_year) + "," + str(myTime.tm_mon-1) + "," + str(myTime.tm_mday),
				minStr = "0" + str(myTime.tm_min) if myTime.tm_min <= 9 and myTime.tm_min != 0 else str(myTime.tm_min)
				secStr = "0" + str(myTime.tm_sec) if myTime.tm_sec <= 9 and myTime.tm_sec != 0 else str(myTime.tm_sec)
				hours = str(myTime.tm_hour)+":"+minStr+":"+secStr
				jsTime = list(myTime)[:6]
				jsTime[1] = jsTime[1] - 1

				retval.append({'type':'history','time':",".join(map(str,jsTime)),'hour':hours,'site':domain,'trans': self.decodeTransition(row[8]),'timeYear':myTime.tm_year,"timeMonth":myTime.tm_mon,"timeDay":myTime.tm_mday})

		# cookie
		conn = sqlite3.connect(os.path.join(self.folderName,"Cookies"))

		for row in conn.execute("SELECT * FROM cookies"):
			if (domainFilter is not None and domainFilter in row[1]) or domainFilter is None:
				epoch = datetime(1601, 1, 1, tzinfo=pytz.UTC)
				cookie_microseconds_since_epoch = row[0]
				cookie_datetime = epoch + timedelta(microseconds=cookie_microseconds_since_epoch)
				ts = time.gmtime(time.mktime(cookie_datetime.timetuple()))
				jsTime = list(ts)[:6]
				jsTime[1] = jsTime[1]-1

				retval.append({"type":"cookie","time":",".join(map(str,jsTime)),'site':row[1],'trans': None})
		return retval
