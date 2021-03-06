from django.db import models
from django.utils import timezone

# Create your models here.

class AccessToken(models.Model):
	""" A model for storing dropbox token information """
	cloudItem = models.ForeignKey('clouditem.CloudItem')
	accessToken = models.TextField(max_length=65535)
	userID = models.CharField(max_length=100)
	serviceType = models.CharField(max_length=10)
	tokenTime = models.DateTimeField(default=timezone.now)
	userInfo = models.TextField()

class FileMetadata(models.Model):
	""" A model for storing file and folders metadata of dropbox """
	metadata = models.TextField()
	tokenID = models.ForeignKey('AccessToken')
	metaTime = models.DateTimeField(default=timezone.now)
	metadataHash = models.TextField(default="-")

class FileDownload(models.Model):
	""" A model for storing if a file has been downloaded or not """

	fileName = models.CharField(max_length=255)
	alternateName = models.CharField(max_length=255)
	status = models.IntegerField()
	downloadTime = models.DateTimeField(default=timezone.now)
	tokenID = models.ForeignKey('AccessToken')
	fileHash = models.TextField(default="-")	

class FileHistory(models.Model):
	""" A model for storing if a file of the history has been downloaded or not """

	revision = models.CharField(max_length=255)
	status = models.IntegerField()
	revisionMetadata = models.TextField()
	fileDownloadID = models.ForeignKey('FileDownload')
	revisionMetadataHash = models.TextField(default="-")
	fileRevisionHash = models.TextField(default="-")
	downloadTime = models.DateTimeField(default=timezone.now)

class Download(models.Model):
	""" A model to keep track of the download """

	tokenID = models.ForeignKey('AccessToken')
	downTime = models.DateTimeField(default=timezone.now)
	endDownTime = models.DateTimeField(null=True,blank=True)
	finalFileSize = models.TextField(default="0")
	folder = models.CharField(max_length=255,blank=True)
	threadStatus = models.IntegerField(default="-1")
	threadMessage = models.TextField(default="-")
	downloadSize = models.BigIntegerField(default=0)
	verificationZIP = models.BooleanField(default=False)
	verificationZIPSignature = models.TextField(default="-")
	verificationZIPSignatureHash = models.TextField(default="-")
	verified = models.BooleanField(default=False)
