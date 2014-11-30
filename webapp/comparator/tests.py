from django.test import TestCase
from django.test.client import Client
from clouditem.models import CloudItem
from downloader.models import AccessToken, FileMetadata, FileDownload, FileHistory,Download
from dashboard.models import MimeType
from django.contrib.auth.models import User
from django.conf import settings
import json,os,urllib,base64
from django.test.utils import override_settings
import fileComparator

class ComparatorTestCase(TestCase):

	def login(self):
		return self.client.login(username="reporter",password="reporter")

	@override_settings(DOWNLOAD_DIR="/media/hd1/testDownloads/")
	@override_settings(DIFF_DIR="/media/hd1/testDiff/")
	def test_comparator_diff_login(self):
		self.assertTrue(self.login())
		url = "/dajaxice/comparator.compareTwoFile/"
		revOne = None
		revTwo = None

		
		for c in CloudItem.objects.all():
			for a in AccessToken.objects.filter(cloudItem=c):

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
							
							payload = {'tokenID': a.id,'cloudItem': c.id,'revOne': revOne,'revTwo': revTwo,'altName': f.alternateName}
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
	
	@override_settings(DIFF_DIR="/media/hd1/testDiff/")
	def test_image_thumbnailer(self):
		self.assertTrue(self.login())

		url = "/dajaxice/comparator.compareTwoFile/"
		cloudItemID = 2
		tokenID = 4
		fileDownloadID = 451
		alternateName = "3ddf4299f1b96c992aa818403c49aa53"

		#get revision
		revs = FileHistory.objects.filter(fileDownloadID=FileDownload.objects.get(id=fileDownloadID))

		revOne = revs[0].revision
		revTwo = revs[1].revision

		payload = {'tokenID': tokenID,'cloudItem': cloudItemID,'revOne': revOne,'revTwo': revTwo,'altName': alternateName}
		data = {"argv": json.dumps(payload)}

		r = self.client.post(url,data=urllib.urlencode(data),secure=True,HTTP_X_REQUESTED_WITH="XMLHttpRequest",content_type="application/x-www-form-urlencoded")
		self.assertEquals(r.status_code,200)
		self.assertContains(r,"aab091a8dad2098fe4645cad6c20ebf4bf4f0a53d76fec6b655f975ce62062fb")
		self.assertContains(r,"5729da77ea013f78619467de1a325223eda4e655e357ea74539be9dc34d9be3f")

		#test if images exists
		imgOnePath = os.path.join(settings.DIFF_DIR,"aab091a8dad2098fe4645cad6c20ebf4bf4f0a53d76fec6b655f975ce62062fb.thumbnail")
		imgTwoPath = os.path.join(settings.DIFF_DIR,"5729da77ea013f78619467de1a325223eda4e655e357ea74539be9dc34d9be3f.thumbnail")
		self.assertTrue(os.path.isfile(imgOnePath))
		self.assertTrue(os.path.isfile(imgTwoPath))

		#delete them
		os.remove(imgOnePath)
		os.remove(imgTwoPath)
	
	@override_settings(DOWNLOAD_DIR="/media/hd1/testDownloads/")
	def test_verifyer_filedownload(self):
		self.assertTrue(self.login())

		for a in AccessToken.objects.all():
			hList = fileComparator.verifyFileDownload(a)

			for i in hList:
				f = FileDownload.objects.get(id=i['fID'])
	
				if f.status == 1:
					self.assertTrue(i['verificationResult'])
				elif f.status == 2:
					self.assertEquals(-1,i['verificationResult'])


	def test_verifyer_metadata(self):
		self.assertTrue(self.login())

		for a in AccessToken.objects.all():
			res = fileComparator.verifyMetadata(a)
			self.assertTrue(res['verificationResult'])

		
