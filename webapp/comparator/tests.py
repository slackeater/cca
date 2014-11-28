from django.test import TestCase
from django.test.client import Client
from clouditem.models import CloudItem
from downloader.models import AccessToken, FileMetadata, FileDownload, FileHistory,Download
from dashboard.models import MimeType
from django.contrib.auth.models import User
from django.conf import settings
import json,os,urllib,base64
from django.test.utils import override_settings

class ComparatorTestCase(TestCase):

	@classmethod
	def setUpClass(self):
		self.ci = CloudItem.objects.all()[0]

	def login(self):
		return self.client.login(username="reporter",password="reporter")

	@override_settings(DOWNLOAD_DIR="/media/hd1/testDownloads/")
	@override_settings(DIFF_DIR="/media/hd1/testDiff/")
	def test_comparator_diff_login(self):
		self.assertTrue(self.login())
		url = "/dajaxice/comparator.compareTwoFile/"
		revOne = None
		revTwo = None

		#test with token one and two
		a1 = AccessToken.objects.get(id=1)
		a2 = AccessToken.objects.get(id=2)

		for a in [a1,a2]:

				for f in FileDownload.objects.filter(tokenID=a):
					fileHistory = FileHistory.objects.filter(fileDownloadID=f)

					#we have at least two versions, we do not need to comapre with original
					if len(fileHistory) > 1:
						#get first and last element
						revOne = fileHistory[0].revision
						revTwo = fileHistory[len(fileHistory)-1].revision
					# only one element in history, compare with original (Dropbox), we will have an exception
					elif len(fileHistory) == 1:
						revOne = fileHistory[0].revision
						revTwo = f.alternateName
				
					if revOne != None and revTwo != None:
						
						payload = {'tokenID': a.id,'cloudItem': self.ci.id,'revOne': revOne,'revTwo': revTwo,'altName': f.alternateName}
						data = {"argv": json.dumps(payload)}
						r = self.client.post(url,data=urllib.urlencode(data),secure=True,HTTP_X_REQUESTED_WITH="XMLHttpRequest",content_type="application/x-www-form-urlencoded")
				
						self.assertEquals(r.status_code,200)
					
						rDump = json.loads(r.content)
						
						if rDump[0]['id'] == "#comparator":
							#error should be empty
							self.assertEquals(rDump[1]['val'], "")

						#empty revOne and revTwo
						revOne = None
						revTwo = None
