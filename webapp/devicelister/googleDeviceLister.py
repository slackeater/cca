from abstractDeviceLister import AbstractDeviceLister
import requests
from lxml.html import fromstring
from pyvirtualdisplay import Display
from selenium import webdriver
class GoogleDeviceLister(AbstractDeviceLister):
	""" This class represent a Google Chrome file browser """

	def __init__(self,token,email,pwd):
		super(GoogleDeviceLister,self).__init__(token,email,pwd)

	def connect(self):
		print "here"
		display = Display(visible=0, size=(1024, 768))
		display.start()
		browser = webdriver.Firefox()
		browser.get('http://www.google.com')
		print "mah"
		print browser.titlebrowser.close()
		display.stop()

		"""session = requests.Session()
		loginPage = "https://accounts.google.com/ServiceLogin?hl=it"
		s = session.get(loginPage)
		html = fromstring(s.content)
		payload = dict(html.forms[0].fields)
		payload.update({'Email':'project2@osgate.org','Passwd':'Gmail.2014'})
		print payload
		url = "https://accounts.google.com/ServiceLoginAuth"
		s = session.post(url,data=payload,allow_redirects=True)
		s = session.get("https://security.google.com/settings/security/activity?pli=1")
		print s.content
		html = fromstring(s.content)
		print html.find_class("hq")"""

	def devList(self):
		pass
