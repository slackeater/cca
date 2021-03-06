from django.test import TestCase
from django.test.client import Client
from clouditem.models import CloudItem
from downloader.models import AccessToken, FileMetadata, FileDownload, FileHistory
from dashboard.models import MimeType
from django.contrib.auth.models import User
from django.conf import settings
import json,os,urllib,base64

class TimelinerTestCase(TestCase):

	def login(self):
		return self.client.login(username="reporter",password="reporter")
	
	def test_timeliner_view_nologin(self):

		for c in CloudItem.objects.all():
			for a in AccessToken.objects.filter(cloudItem=c):
				resp = self.client.get('/timeliner/'+str(c.id)+'/'+str(a.id)+'/',follow=True,secure=True)
				self.assertRedirects(resp,"/login/")

	def test_timeliner_view_login(self):
		self.assertTrue(self.login())

		for c in CloudItem.objects.all():
			for a in AccessToken.objects.filter(cloudItem=c):
				resp = self.client.get('/timeliner/'+str(c.id)+'/'+str(a.id)+'/',secure=True)
				self.assertContains(resp,"Documents timeline")

	def test_timeliner_ci_notexist_login(self):
		self.assertTrue(self.login())

		with self.assertRaises(CloudItem.DoesNotExist):
			self.client.get('/timeliner/1000/33/',secure=True)

	def test_timeliner_token_notexist_login(self):
		self.assertTrue(self.login())

		with self.assertRaises(AccessToken.DoesNotExist):
			for c in CloudItem.objects.all():
				self.client.get('/timeliner/'+str(c.id)+'/1000/',secure=True)

	def test_timeliner_showtimeline_login(self):
		self.assertTrue(self.login())
		url = "/dajaxice/timeliner.formTimeliner/"

		for c in CloudItem.objects.all():
			for a in AccessToken.objects.filter(cloudItem=c):
			
				# deleted
				payload = {'tokenID': a.id, "cloudItem": c.id,"form":"resType=0&mimeType=1090"}
				data = {"argv": json.dumps(payload)}
				r = self.client.post(url,data=urllib.urlencode(data),secure=True,HTTP_X_REQUESTED_WITH="XMLHttpRequest",content_type="application/x-www-form-urlencoded")
				self.assertEquals(r.status_code,200)

				rDump = json.loads(r.content)
			
				if a.id == 3:
					self.assertEqual(rDump[0]['id'],"#formHistoryError")
				else: 
					self.assertEqual(rDump[0]['id'],"#formHistory")
					self.assertEqual(rDump[1]['val'], "")

				#all
				payload = {'tokenID': a.id, "cloudItem": c.id,"form":"resType=2&mimeType=1090"}
				data = {"argv": json.dumps(payload)}
				r = self.client.post(url,data=urllib.urlencode(data),secure=True,HTTP_X_REQUESTED_WITH="XMLHttpRequest",content_type="application/x-www-form-urlencoded")
				self.assertEquals(r.status_code,200)

				rDump = json.loads(r.content)
				self.assertEqual(rDump[0]['id'],"#formHistory")
				self.assertEqual(rDump[1]['val'], "")

				#mime type

				if a.id == 1:
					mime = "1229"
				elif a.id == 2:
					mime = "174"
				elif a.id == 3:
					mime = "1153"
				elif a.id == 4:
					mime = "217"

				payload = {'tokenID': a.id, "cloudItem": c.id,"form":"resType=1&mimeType="+mime+""}
				data = {"argv": json.dumps(payload)}
				r = self.client.post(url,data=urllib.urlencode(data),secure=True,HTTP_X_REQUESTED_WITH="XMLHttpRequest",content_type="application/x-www-form-urlencoded")
				self.assertEquals(r.status_code,200)

				rDump = json.loads(r.content)

				self.assertEqual(rDump[0]['id'],"#formHistory")
				self.assertEqual(rDump[1]['val'], "")

	def test_timeliner_showhistory_login(self):
		self.assertTrue(self.login())
		url = "/dajaxice/timeliner.fileHistoryTimeliner/"

		for c in CloudItem.objects.all():
			for a in AccessToken.objects.filter(cloudItem=c):

				#get all files for this token
				files = FileDownload.objects.filter(tokenID=a)

				for f in files:
					#get history for this file

					payload = {'tokenID': a.id, "cloudItem": c.id,"altName":str(f.alternateName)}
					data = {"argv": json.dumps(payload)}
					r = self.client.post(url,data=urllib.urlencode(data),secure=True,HTTP_X_REQUESTED_WITH="XMLHttpRequest",content_type="application/x-www-form-urlencoded")
					rDump = json.loads(r.content)
					
					self.assertEquals(r.status_code,200)

					#fh = FileHistory.objects.filter(fileDownloadID=f)

					#we have a history
					if rDump[0]['id'] == "#fileHistory":
						# history element present and no error
						self.assertEqual(rDump[1]['val'], "")
					elif rDump[0]['id'] == "#formHistoryError":
						# error element if no history
						self.assertEquals(rDump[0]['val'],"No history for this file")
