from django.test import TestCase
from django.test.client import Client
from clouditem.models import CloudItem
from downloader.models import AccessToken, FileMetadata
from dashboard.models import MimeType
from importer.models import Upload
from django.contrib.auth.models import User
from django.conf import settings
import json,os,urllib
from django.test.utils import override_settings

class ImporterTestCase(TestCase):

	def login(self):
		return self.client.login(username="reporter",password="reporter")

	def test_importer_view_nologin(self):
		for c in CloudItem.objects.all():
			r = self.client.get("/importer/"+str(c.id)+"/",secure=True,follow=True)
			self.assertRedirects(r,"/login/")

	def test_importer_view_login(self):
		self.assertTrue(self.login())

		for c in CloudItem.objects.all():
			r = self.client.get("/importer/"+str(c.id)+"/",secure=True)
			self.assertEqual(r.status_code,200)
			self.assertContains(r,"Report")

	@override_settings(UPLOAD_DIR="/media/hd1/testUploads/")
	def test_importer_import(self):
		self.assertTrue(self.login())

		fileName = "7537275ab89084c1d8c0f99381ad30c5"
		fileImport = os.path.join(settings.BASE_DIR,"webapp","tests",fileName+".zip.enc")

		for c in CloudItem.objects.all():
			with open(fileImport,"rb") as fp:
				r = self.client.post("/importer/"+str(c.id)+"/",data={'fileUp': fp},secure=True)
				self.assertEquals(r.status_code,200)
				self.assertContains(r,fileName)

			url = "/dajaxice/importer.showReport/"
			
			up = Upload.objects.get(cloudItemID=c)
			payload = {"up":up.id,"ci":c.id}
			data = {"argv": json.dumps(payload)}
			r = self.client.post(url,urllib.urlencode(data),secure=True,HTTP_X_REQUESTED_WITH="XMLHttpRequest",content_type="application/x-www-form-urlencoded")
			
			self.assertEquals(r.status_code,200)
			self.assertContains(r,"John-PC")
			self.assertContains(r,"Windows")
			self.assertContains(r,"One Drive 17.3.1229.0918")

	def test_importer_notexist_login(self):
		self.assertTrue(self.login())

		with self.assertRaises(CloudItem.DoesNotExist):
			self.client.get("/importer/3000/",secure=True)

	@override_settings(UPLOAD_DIR="/media/hd1/testUploads/")
	def test_importer_import_nonzip_login(self):
		self.assertTrue(self.login())

		fileName = "1ac584b00c5091e9a74b8c23ba745258"
		fileImport = os.path.join(settings.BASE_DIR,"webapp","tests",fileName+".zip.enc")

		for c in CloudItem.objects.all():
			with open(fileImport,"rb") as fp:
				r = self.client.post("/importer/"+str(c.id)+"/",data={'fileUp': fp},secure=True)
				self.assertEquals(r.status_code,200)
				self.assertContains(r,"No JSON object could be decoded")
			
