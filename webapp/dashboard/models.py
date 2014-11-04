from django.db import models
from django.utils import timezone

# Create your models here.

class DropboxToken(models.Model):
	""" A model for storing dropbox token information """
	importID = models.ForeignKey('importer.Upload')
	accessToken = models.CharField(max_length=256)
	userID = models.CharField(max_length=20)

class GDriveToken(models.Model):
	""" A model for storing gdrive token information """
	
