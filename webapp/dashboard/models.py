from django.db import models
from django.utils import timezone

# Create your models here.

class DropboxToken(models.Model):
	""" A model for storing dropbox token information """
	importID = models.ForeignKey('importer.Upload')
	accessToken = models.CharField(max_length=256)
	userID = models.CharField(max_length=20)

class DropboxFileMetadata(models.Model):
	""" A model for storing file and folders metadata of dropbox """
	metadata = models.CharField(max_length=16384)
	tokenID = models.ForeignKey('DropboxToken')
	metaTime = models.DateTimeField(default=timezone.now, blank=True)

class DropboxAccountInfo(models.Model):
	""" A model for storing user info """
	accountInfo = models.TextField(max_length=16777215)
	tokenID = models.ForeignKey("DropboxToken")
	metaTime = models.DateTimeField(default=timezone.now, blank=True)

class MimeType(models.Model):
	""" A model for storing MIME types """
	mime = models.CharField(max_length=100)
