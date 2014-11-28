from django.db import models
from django.utils import timezone

# Create your models here.

class Upload(models.Model):
	fileName = models.CharField(max_length=256)
	uploadDate = models.DateTimeField(default=timezone.now, blank=True)
	uploadIP = models.IPAddressField(default="0.0.0.0",blank=True)
	parsed = models.BooleanField(default=False)
	cloudItemID = models.ForeignKey("clouditem.CloudItem")
