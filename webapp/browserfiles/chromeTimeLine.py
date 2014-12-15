from abstractFileTimeLine import AbstractFileTimeLine

class GoogleChromeFileTimeLine(AbstractFileTimeLine):

	def __init__(self,historyFile,cookieFile):
		AbstractFileTimeLine.__init__(self,historyFile,cookieFile)

	def constructTimeLineItem(self):
		return

	def generateTimeLine(self):
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

	def docmentsHistoryTimeline(self):
		""" Generate a list of browse history """
		
		conn = sqlite3.connect(self.h)

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
