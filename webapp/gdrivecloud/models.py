from django.db import models
from dashboard.models import GoogleDriveToken
from django.utils import timezone

# Create your models here.

class GoogleAccountInfo(models.Model):
	""" Model for storing google account information """
	accountInfo = models.TextField()
	tokenID = models.ForeignKey("dashboard.GoogleDriveToken")
	metaTime = models.DateTimeField(default=timezone.now, blank=True)
