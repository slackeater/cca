from django.test import TestCase
from django.test.client import Client
from clouditem.models import CloudItem
from downloader.models import AccessToken, FileMetadata, FileDownload
from dashboard.models import MimeType
from django.contrib.auth.models import User
from django.conf import settings
import json,os,urllib

class CloudserviceTestCase(TestCase):

	def login(self):
		return self.client.login(username="reporter",password="reporter")
	
	def test_analyse_view_nologin(self):
		for c in CloudItem.objects.all():

			#get acccess token
			for a in AccessToken.objects.filter(cloudItem=c):
				resp = self.client.get('/analyse/'+str(c.id)+'/'+str(a.id)+'/',follow=True,secure=True)
				self.assertRedirects(resp,"/login/")

	def test_analyse_view_login(self):
		self.assertTrue(self.login())

		for c in CloudItem.objects.all():

			#get acccess token
			for a in AccessToken.objects.filter(cloudItem=c):
				resp = self.client.get('/analyse/'+str(c.id)+'/'+str(a.id)+'/',follow=True,secure=True)
				self.assertContains(resp,a.serviceType.title())

	def test_analyse_ci_notexist_login(self):
		self.assertTrue(self.login())

		with self.assertRaises(CloudItem.DoesNotExist):
			self.client.get('/analyse/1000/33/',secure=True)

	def test_analyse_token_notexist_login(self):
		self.assertTrue(self.login())

		with self.assertRaises(AccessToken.DoesNotExist):
			for c in CloudItem.objects.all():
				self.client.get('/analyse/'+str(c.id)+'/1000/',secure=True)

	def test_analyse_metadata(self):
		self.assertTrue(self.login())
	
		for c in CloudItem.objects.all():
			for a in AccessToken.objects.filter(cloudItem=c):
				payload = {"tokenID":a.id,"cloudItem":c.id}
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

		for c in CloudItem.objects.all():
			for a in AccessToken.objects.filter(cloudItem=c):
				url = "/dajaxice/cloudservice.searchMetaData/"

				# deleted
				payload = {'tokenID': a.id, "cloudItem": c.id,"form":"resType=0&mimeType=1090"}
				data = {"argv": json.dumps(payload)}
				r = self.client.post(url,data=urllib.urlencode(data),secure=True,HTTP_X_REQUESTED_WITH="XMLHttpRequest",content_type="application/x-www-form-urlencoded")
				self.assertEquals(r.status_code,200)

				rDump = json.loads(r.content)
				self.assertEqual(rDump[0]['id'],"#searchRes")
				self.assertEqual(rDump[1]['val'], "")

				#all
				payload = {'tokenID': a.id, "cloudItem": c.id,"form":"resType=2&mimeType=1090"}
				data = {"argv": json.dumps(payload)}
				r = self.client.post(url,data=urllib.urlencode(data),secure=True,HTTP_X_REQUESTED_WITH="XMLHttpRequest",content_type="application/x-www-form-urlencoded")
				self.assertEquals(r.status_code,200)

				rDump = json.loads(r.content)
				self.assertEqual(rDump[0]['id'],"#searchRes")
				self.assertEqual(rDump[1]['val'], "")

				#mime type
				payload = {'tokenID': a.id, "cloudItem": c.id,"form":"resType=1&mimeType=1228"}
				data = {"argv": json.dumps(payload)}
				r = self.client.post(url,data=urllib.urlencode(data),secure=True,HTTP_X_REQUESTED_WITH="XMLHttpRequest",content_type="application/x-www-form-urlencoded")
				self.assertEquals(r.status_code,200)
				
				rDump = json.loads(r.content)
				self.assertEqual(rDump[0]['id'],"#searchRes")
				self.assertEqual(rDump[1]['val'], "")

	def test_analyse_fileinfo(self):
		self.assertTrue(self.login())


		for c in CloudItem.objects.all():
			for a in AccessToken.objects.filter(cloudItem=c):
				url = "/dajaxice/cloudservice.fileInfo/"

				files = FileDownload.objects.filter(tokenID=a)

				for f in files:
					#make a request for each file
					payload = {"tokenID": a.id,"cloudItem": c.id,"id":str(f.alternateName)}
					data = {"argv": json.dumps(payload)}
					r = self.client.post(url,data=urllib.urlencode(data),secure=True,HTTP_X_REQUESTED_WITH="XMLHttpRequest",content_type="application/x-www-form-urlencoded")
					self.assertEquals(r.status_code,200)
					self.assertContains(r,f.alternateName)

	def test_analyse_filerevision(self):
		self.assertTrue(self.login())

		for c in CloudItem.objects.all():
			for a in AccessToken.objects.filter(cloudItem=c):
				url = "/dajaxice/cloudservice.fileRevision/"

				files = FileDownload.objects.filter(tokenID=a)

				for f in files:
					#make a request for each file
					payload = {"tokenID": a.id,"cloudItem": c.id,"fId":str(f.alternateName)}
					data = {"argv": json.dumps(payload)}
					r = self.client.post(url,data=urllib.urlencode(data),secure=True,HTTP_X_REQUESTED_WITH="XMLHttpRequest",content_type="application/x-www-form-urlencoded")
					self.assertEquals(r.status_code,200)
					
					#check that there are not errros
					rDump = json.loads(r.content)
					self.assertEquals(rDump[1]['val'],"")
