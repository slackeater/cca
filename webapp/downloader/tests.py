from django.test import TestCase,TransactionTestCase
from django.test.client import Client
from clouditem.models import CloudItem
from downloader.models import *
from models import AccessToken
import json,urllib,threading,zipfile,os,base64,binascii,sys
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from webapp.dbMaker import MakeDatabase
from threadmanager import ThreadManager
from webapp import constConfig
from django.test.utils import override_settings
from django.conf import settings
from verifier import Verifier

class DownloaderThreadTestCase(TransactionTestCase):

	def test_downloader_full(self):

		#google and dropbox token
		tList = [1,2]

		for tokenID in tList:
			t = ThreadManager(tokenID,True)
			instance = t.download()
			instance.join()

			#check all different steps
			statusList = t.statusList
			self.assertEquals(constConfig.THREAD_INIT,statusList[0].threadStatus)
			self.assertEquals(constConfig.THREAD_DOWN,statusList[1].threadStatus)
			self.assertEquals(constConfig.THREAD_PHASE_1,statusList[2].threadStatus)
			self.assertEquals(constConfig.THREAD_PHASE_2,statusList[3].threadStatus)
			self.assertEquals(constConfig.THREAD_PHASE_3,statusList[4].threadStatus)

			#database status should be 3, everything has been downloaded
			dStatus = Download.objects.get(tokenID=AccessToken.objects.get(id=tokenID))
			self.assertEquals(constConfig.THREAD_PHASE_3,dStatus.threadStatus)

class DownloaderTestCase(TestCase):

	def login(self):
		return self.client.login(username="reporter",password="reporter")
	
	def test_token_cloudview_nologin(self):
		resp = self.client.get('/token/2000/',follow=True,secure=True)
		self.assertRedirects(resp,"/login/")

	def test_token_view_login(self):
		self.assertTrue(self.login())
	
		for c in CloudItem.objects.all():
			resp = self.client.get("/token/"+str(c.id)+"/",secure=True)
			self.assertContains(resp,"Dropbox")
			self.assertContains(resp,"Google Drive")

	def test_token_cloudtokenview_nologin(self):
		for c in CloudItem.objects.all():
			resp = self.client.get("/token/"+str(c.id)+"/8000/",follow=True,secure=True)
			self.assertRedirects(resp,"/login/")

	def test_token_view_notexist_login(self):
		self.assertTrue(self.login())

		with self.assertRaises(CloudItem.DoesNotExist):
			self.client.get("/token/2000/",secure=True)

	def test_token_dash_login(self):
		self.assertTrue(self.login())

		for c in CloudItem.objects.all():
			for at in AccessToken.objects.filter(cloudItem=c):
				resp = self.client.get("/token/"+str(c.id)+"/"+str(at.id)+"/",secure=True)
				self.assertContains(resp,"Download")
				self.assertContains(resp,"Metadata")
				self.assertContains(resp,"Timelines")
				self.assertContains(resp,"Report")

	def test_download_view_nologin(self):
		for c in CloudItem.objects.all():
			for at in AccessToken.objects.filter(cloudItem=c):
				resp = self.client.get("/download/"+str(c.id)+"/"+str(at.id)+"/",secure=True,follow=True)
				self.assertRedirects(resp,"/login/")

	def test_download_view_login(self):
		self.assertTrue(self.login())

		for c in CloudItem.objects.all():
			for at in AccessToken.objects.filter(cloudItem=c):
				resp = self.client.get("/download/"+str(c.id)+"/"+str(at.id)+"/",secure=True)
				self.assertContains(resp,"The download will include")

	def test_download_view_cinotexist_login(self):
		self.assertTrue(self.login())

		with self.assertRaises(CloudItem.DoesNotExist):
			self.client.get("/download/2000/1/",secure=True)

	def test_download_view_tknnotexist_login(self):
		self.assertTrue(self.login())

		for ci in CloudItem.objects.all():
			with self.assertRaises(AccessToken.DoesNotExist):
				self.client.get("/download/"+str(ci.id)+"/1000/",secure=True)

	def test_show_tokens_dropbox_login(self):
		self.assertTrue(self.login())

		url = "/dajaxice/downloader.showDropboxTokens/"

		c = CloudItem.objects.get(id=2)
		payload = {"ci":c.id}
		data = {"argv": json.dumps(payload)}
		r = self.client.post(url,urllib.urlencode(data),secure=True,HTTP_X_REQUESTED_WITH="XMLHttpRequest",content_type="application/x-www-form-urlencoded")
		self.assertEquals(r.status_code,200)

		self.assertContains(r,"151315309")
		self.assertContains(r,"358059925")

	def test_show_tokens_google_login(self):
		self.assertTrue(self.login())

		c = CloudItem.objects.get(id=1)
		url = "/dajaxice/downloader.showGoogleTokens/"
		payload = {"ci":c.id}
		data = {"argv": json.dumps(payload)}
		r = self.client.post(url,urllib.urlencode(data),secure=True,HTTP_X_REQUESTED_WITH="XMLHttpRequest",content_type="application/x-www-form-urlencoded")

		self.assertEquals(r.status_code,200)
		self.assertContains(r,"114260070272708105141")
		self.assertContains(r,"112263419935383071563")
		

	def test_downloader_view(self):

		self.assertTrue(self.login())

		tokenID = 1
		ci = 1

		#first get the normal page
		r = self.client.get("/download/"+str(ci)+"/"+str(tokenID)+"/",secure=True)

		self.assertEquals(r.status_code,200)
		self.assertContains(r,"Download already completed")

		#this download has already been made
		d = Download.objects.get(tokenID=AccessToken.objects.get(id=tokenID))
		self.assertEquals(constConfig.THREAD_PHASE_3,d.threadStatus)

	def test_downloader_view_new_download(self):
		self.assertTrue(self.login())
		ci = 1
		at = 5
	
		newToken = AccessToken(id=at,accessToken="testToken",userID="0",serviceType="google",tokenTime=timezone.now(),userInfo="noInfo",cloudItem=CloudItem.objects.get(id=ci))
		newToken.save()

		#first get the normal page 
		r = self.client.get("/download/"+str(ci)+"/"+str(at)+"/",secure=True)
		
		self.assertContains(r,"No download have been started")

		#take last download
		d = Download.objects.latest("downTime")

		self.assertEquals(at,d.tokenID.id)
		#button has not been click
		self.assertEquals(constConfig.THREAD_NOTCLICKED,d.threadStatus)

	@override_settings(DOWNLOAD_DIR="/media/hd1/testDownloads")
	@override_settings(VERIFIED_ZIP="/media/hd1/verifiedZIPtest")
	def test_zip_verifier(self):

		token = AccessToken.objects.get(id=4)

		zipName = Download.objects.get(tokenID=token).folder
		v = Verifier(token)
		v.createZIPtoVerify()

		#now the DB should be updated
		dUp = Download.objects.get(tokenID=token)
		self.assertTrue(dUp.verificationZIP)
		
		#now create the same zip and verify the signatures
		"""tempZip = os.path.join(settings.VERIFIED_ZIP,zipName+".zip.test")
		newVerifier = Verifier(token)
		newVerifier.createZIP(".zip.test")

		# add path for crypto
		cryptoPath = os.path.join(os.path.dirname(settings.BASE_DIR), "finder")

		if not cryptoPath in sys.path:
			sys.path.insert(1, cryptoPath)
			del cryptoPath

		import crypto

		#verify the signature
		h = crypto.sha256File(tempZip)
		res = crypto.verifyRSAsignatureSHA256(h,dUp.verificationZIPSignatureHash,settings.PUB_KEY)

		self.assertTrue(res)
		"""
		#generate a timestamp request
		v.createTimestampRequest()

		requestCreated = os.path.isfile(os.path.join(settings.VERIFIED_ZIP,dUp.folder+".tsrequest"))

		self.assertTrue(requestCreated)
