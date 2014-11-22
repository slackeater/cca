from django.test import TestCase
from django.test.client import Client
from clouditem.models import CloudItem
from downloader.models import AccessToken, FileMetadata
from dashboard.models import MimeType
from django.contrib.auth.models import User
from django.conf import settings
import json,os,urllib
from webapp.dbMaker import MakeDatabase
class DownloaderTestCase(TestCase):

	@classmethod
	def setUpClass(self):
		self.ci = CloudItem.objects.all()[0]

	def login(self):
		return self.client.login(username="reporter",password="reporter")
	
	def test_analyse_view_nologin(self):
		for a in AccessToken.objects.all():
			resp = self.client.get('/analyse/'+str(self.ci.id)+'/'+str(a.id)+'/',follow=True,secure=True)
			self.assertRedirects(resp,"/login/")

	def test_analyse_view_login(self):
		self.assertTrue(self.login())
		
		

		for a in AccessToken.objects.all():
			resp = self.client.get('/analyse/'+str(self.ci.id)+'/'+str(a.id)+'/',secure=True)
			self.assertContains(resp,a.serviceType.title())

	def test_analyse_ci_notexist_login(self):
		self.assertTrue(self.login())

		with self.assertRaises(CloudItem.DoesNotExist):
			self.client.get('/analyse/1000/33/',secure=True)

	def test_analyse_token_notexist_login(self):
		self.assertTrue(self.login())

		with self.assertRaises(AccessToken.DoesNotExist):
			self.client.get('/analyse/'+str(self.ci.id)+'/1000/',secure=True)

	def test_analyse_metadata(self):
		self.assertTrue(self.login())
		
		for a in AccessToken.objects.all():
			payload = {"tokenID":a.id,"cloudItem":self.ci.id}
			data = {'argv': json.dumps(payload)}

			r = self.client.post(
					"/dajaxice/cloudservice.metadataAnalysis/",
					data=urllib.urlencode(data),
					secure=True,
					HTTP_X_REQUESTED_WITH='XMLHttpRequest',
					content_type="application/x-www-form-urlencoded"
			)
			
			rDump = json.loads(r.content)
			
			self.assertEqual(rDump[0]['id'],"#metaAnalysis")
			#error should be empty
			self.assertEqual(rDump[1]['val'],"")

	def test_analyse_searchmetadata(self):
		self.assertTrue(self.login())

		for a in AccessToken.objects.all():
			url = "/dajaxice/cloudservice.searchMetaData/"

			# deleted
			payload = {'tokenID': a.id, "cloudItem": self.ci.id,"form":"resType=0&mimeType=1090"}
			data = {"argv": json.dumps(payload)}
			r = self.client.post(url,data=urllib.urlencode(data),secure=True,HTTP_X_REQUESTED_WITH="XMLHttpRequest",content_type="application/x-www-form-urlencoded")
			self.assertEquals(r.status_code,200)

			rDump = json.loads(r.content)
			self.assertEqual(rDump[0]['id'],"#searchRes")
			self.assertEqual(rDump[1]['val'], "")

			#all
			payload = {'tokenID': a.id, "cloudItem": self.ci.id,"form":"resType=2&mimeType=1090"}
			data = {"argv": json.dumps(payload)}
			r = self.client.post(url,data=urllib.urlencode(data),secure=True,HTTP_X_REQUESTED_WITH="XMLHttpRequest",content_type="application/x-www-form-urlencoded")
			self.assertEquals(r.status_code,200)

			rDump = json.loads(r.content)
			self.assertEqual(rDump[0]['id'],"#searchRes")
			self.assertEqual(rDump[1]['val'], "")

			#mime type
			payload = {'tokenID': a.id, "cloudItem": self.ci.id,"form":"resType=1&mimeType=1228"}
			data = {"argv": json.dumps(payload)}
			r = self.client.post(url,data=urllib.urlencode(data),secure=True,HTTP_X_REQUESTED_WITH="XMLHttpRequest",content_type="application/x-www-form-urlencoded")
			self.assertEquals(r.status_code,200)
			
			rDump = json.loads(r.content)
			self.assertEqual(rDump[0]['id'],"#searchRes")
			self.assertEqual(rDump[1]['val'], "")
