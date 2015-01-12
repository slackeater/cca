from abstractBrowserFile import AbstractBrowserFile
import os,sqlite3,urlparse,time,pytz
from datetime import datetime,timedelta

class FirefoxFiles(AbstractBrowserFile):
	""" This class represent a Google Chrome file browser """

	def __init__(self,folderPath,profile):
		self.folderName = os.path.join(folderPath,"firefox-copy",profile)
		print self.folderName
		AbstractBrowserFile.__init__(self)

	def constructTimeLineItem(self):
		return

	def generateTimeLine(self,domainFilter):
		""" Generate a list of browse history """
		print os.path.join(self.folderName,"places.sqlite")	
		conn = sqlite3.connect(os.path.join(self.folderName,"places.sqlite"))
		retval = list()

		# history
		for row in conn.execute("SELECT datetime(moz_historyvisits.visit_date/1000000,'unixepoch'), moz_places.url FROM moz_places, moz_historyvisits WHERE moz_places.id = moz_historyvisits.place_id"):
			print row

			"""if (domainFilter is not None and domainFilter in row[0]) or domainFilter is None:
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
		return retval"""
