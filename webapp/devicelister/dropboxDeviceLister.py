from abstractDeviceLister import AbstractDeviceLister
import requests
from lxml.html import fromstring
from ghost import Ghost

class DropboxDeviceLister(AbstractDeviceLister):

	def __init__(self,token,email,pwd):
		super(DropboxDeviceLister,self).__init__(token,email,pwd)

	def connect(self):
                print "HHUUUUU"
                ghost = Ghost()
                loginPage = "https://www.dropbox.com/login"
                page, resources = ghost.open(loginPage)
                print "UUUUU"
                print page
                result, resources = ghost.fill("login-form",{'login_email':'project2@osgate.org','password':'Dropbox.2014'})
                page, resources = ghost.fire("login-form","submit",expect_loading=True)
                print page

		"""session = requests.Session()
                loginPage = "https://www.dropbox.com/login"
		s = session.get(loginPage)
		html = fromstring(s.content)
		payload = dict(html.forms[0].fields)
		payload.update({'login_email':'project2@osgate.org','login_password':'Dropbox.2014'})

                thirdDict = dict(html.forms[2].fields)
                payload.update({"t":thirdDict["t"]})
		print payload
                s = session.post("https://www.dropbox.com/ajax_login",data=payload,allow_redirects=True)
                s = session.get("https://www.dropbox.com/account")
                print s.content
                """
	def devList(self):
		pass
