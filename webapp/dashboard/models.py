from django.db import models
from django.utils import timezone

# Create your models here.

class AccessToken(models.Model):
	""" A model for storing dropbox token information """
	importID = models.ForeignKey('importer.Upload')
	accessToken = models.TextField(max_length=65535)
	userID = models.CharField(max_length=100)
	serviceType = models.CharField(max_length=10)
	tokentime = models.DateTimeField(default=timezone.now)

class FileMetadata(models.Model):
	""" A model for storing file and folders metadata of dropbox """
	metadata = models.TextField()
	tokenID = models.ForeignKey('AccessToken')
	metaTime = models.DateTimeField(default=timezone.now, blank=True)

class AccountInfo(models.Model):
	""" A model for storing user info """
	accountInfo = models.TextField()
	tokenID = models.ForeignKey("AccessToken")
	metaTime = models.DateTimeField(default=timezone.now, blank=True)

class MimeType(models.Model):
	""" A model for storing MIME types """
	mime = models.CharField(max_length=100)
