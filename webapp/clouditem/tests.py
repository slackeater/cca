from django.test import TestCase
from django.test.client import Client
from django.core.exceptions import ObjectDoesNotExist
import views
from models import CloudItem
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

class CloudItemTestCase(TestCase):

	def setUp(self):
		self.user = User.objects.create_user(username="reporter",password='reporter',email="rep@rep.com")
		
		ci = CloudItem(desc="Set up clouditem",reportName="Set up",reporterID=self.user)
		ci.save()

	def test_clouditem_view_nologin(self):
		resp = self.client.get('/clouditem/',follow=True,secure=True)
		self.assertRedirects(resp,"/login/")
		resp = self.client.post('/clouditem/',follow=True,secure=True)
		self.assertRedirects(resp,"login/")

	def test_clouditem_view_login(self):
		
		resp = self.client.login(username="reporter",password="reporter")
		self.assertTrue(resp)
		resp = self.client.get('/clouditem/',secure=True)
		self.assertEquals(resp.status_code,200)

	def test_clouditem_view_instertion(self):
		# login and display of clouditem page
		resp = self.client.login(username="reporter",password="reporter")
		self.assertTrue(resp)
		resp = self.client.get('/clouditem/',secure=True)
		self.assertEquals(resp.status_code,200)

		#insert clouditem
		resp = self.client.post("/clouditem/",{'name':'test scan','description':'scan of a suspect test'},secure=True)
		self.assertContains(resp,"scan of a suspect test")

	def test_showclouditem_view_nologin(self):
		resp = self.client.get('/clouditem/29/',follow=True,secure=True)
		self.assertRedirects(resp,"/login/")
		resp = self.client.post('/clouditem/29/',follow=True,secure=True)
		self.assertRedirects(resp,"login/")
	
	def test_showclouditem_view_login(self):
		resp = self.client.login(username="reporter",password="reporter")
		self.assertTrue(resp)
	
		for c in CloudItem.objects.all():
			resp = self.client.get('/clouditem/'+str(c.id)+'/',secure=True)
			self.assertContains(resp,"Choose one of the functionalities below:")
	
	def test_showclouditem_notexist_login(self):
		resp = self.client.login(username="reporter",password="reporter")
		self.assertTrue(resp)
		
		with self.assertRaises(CloudItem.DoesNotExist):
			self.client.get('/clouditem/200/',secure=True)
