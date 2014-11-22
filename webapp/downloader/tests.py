from django.test import TestCase
from django.test.client import Client
from clouditem.models import CloudItem
from models import AccessToken
import json,urllib
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from webapp.dbMaker import MakeDatabase

class DownloaderTestCase(TestCase):

	@classmethod
	def setUpClass(self):
		"""db = MakeDatabase()

		db.createUser()
		db.createCloudItem()
		db.createAccessToken()"""

		self.ci = CloudItem.objects.all()[0]

	def login(self):
		return self.client.login(username="reporter",password="reporter")
	
	def test_token_cloudview_nologin(self):
		resp = self.client.get('/token/2000/',follow=True,secure=True)
		self.assertRedirects(resp,"/login/")

	def test_token_view_login(self):
		self.assertTrue(self.login())
		
		resp = self.client.get("/token/"+str(self.ci.id)+"/",secure=True)
		self.assertContains(resp,"Dropbox")
		self.assertContains(resp,"Google Drive")

	def test_token_cloudtokenview_nologin(self):
		resp = self.client.get("/token/"+str(self.ci.id)+"/8000/",follow=True,secure=True)
		self.assertRedirects(resp,"/login/")

	def test_token_view_notexist_login(self):
		self.assertTrue(self.login())

		with self.assertRaises(CloudItem.DoesNotExist):
			self.client.get("/token/2000/",secure=True)

	def test_token_dash_login(self):
		self.assertTrue(self.login())

		for at in AccessToken.objects.all():
			resp = self.client.get("/token/"+str(self.ci.id)+"/"+str(at.id)+"/",secure=True)
			self.assertContains(resp,"Download")
			self.assertContains(resp,"Metadata")
			self.assertContains(resp,"Timelines")
			self.assertContains(resp,"Report")

	def test_download_view_nologin(self):
		for at in AccessToken.objects.all():
			resp = self.client.get("/download/"+str(self.ci.id)+"/"+str(at.id)+"/",secure=True,follow=True)
			self.assertRedirects(resp,"/login/")

	def test_download_view_login(self):
		self.assertTrue(self.login())

		for at in AccessToken.objects.all():
			resp = self.client.get("/download/"+str(self.ci.id)+"/"+str(at.id)+"/",secure=True)
			self.assertContains(resp,"The download will include")

	def test_download_view_cinotexist_login(self):
		self.assertTrue(self.login())

		with self.assertRaises(CloudItem.DoesNotExist):
			self.client.get("/download/2000/1/",secure=True)

	def test_download_view_tknnotexist_login(self):
		self.assertTrue(self.login())

		with self.assertRaises(AccessToken.DoesNotExist):
			self.client.get("/download/"+str(self.ci.id)+"/1000/",secure=True)

	def test_show_tokens_dropbox_login(self):
		self.assertTrue(self.login())

		url = "/dajaxice/downloader.showDropboxTokens/"
		payload = {"ci":self.ci.id}
		data = {"argv": json.dumps(payload)}
		r = self.client.post(url,urllib.urlencode(data),secure=True,HTTP_X_REQUESTED_WITH="XMLHttpRequest",content_type="application/x-www-form-urlencoded")
		self.assertEquals(r.status_code,200)

		self.assertContains(r,"151315309")
		self.assertContains(r,"358059925")

	def test_show_tokens_google_login(self):
		self.assertTrue(self.login())

		url = "/dajaxice/downloader.showGoogleTokens/"
		payload = {"ci":self.ci.id}
		data = {"argv": json.dumps(payload)}
		r = self.client.post(url,urllib.urlencode(data),secure=True,HTTP_X_REQUESTED_WITH="XMLHttpRequest",content_type="application/x-www-form-urlencoded")

		self.assertEquals(r.status_code,200)
		self.assertContains(r,"114260070272708105141")
		self.assertContains(r,"112263419935383071563")
		
