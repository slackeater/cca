from abstractDeviceLister import AbstractDeviceLister
import requests

class GoogleDeviceLister(AbstractDeviceLister):
	""" This class represent a Google Chrome file browser """

	def __init__(self,token,email,pwd):
		super(GoogleDeviceLister,self).__init__(token,email,pwd)

	def connect(self):
		url = "https://accounts.google.com/ServiceLoginAuth"
		session = requests.Session()
		s = session.post(url,data={'Email':'project2@osgate.org','Passwd':'Gmail.2014'},allow_redirects=True)
		print s.text
		s = session.get("https://security.google.com/settings/security/activity?pli=1")
		pass

	def devList(self):
		pass
