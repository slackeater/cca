from django.db import models
from django.utils import timezone
# Create your models here.


class CloudItem(models.Model):
	""" A model used to represent a cloud item """

	reporterName = models.CharField(max_length=20)
	itemTime = models.DateTimeField(default=timezone.now)
	importID = models.ForeignKey("importer.Upload",null=True)
	#downloadID = models.ForeignKey("downloader.Download",null=True)
	#TODO Report
	desc = models.TextField()
	reportName = models.CharField(max_length=20)
	

