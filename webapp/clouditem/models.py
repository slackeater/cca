from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
# Create your models here.


class CloudItem(models.Model):
	""" A model used to represent a cloud item """

	itemTime = models.DateTimeField(default=timezone.now)
	#downloadID = models.ForeignKey("downloader.Download",null=True)
	#TODO Report
	desc = models.TextField()
	reportName = models.CharField(max_length=20)
	reporterID = models.ForeignKey(User)
	

