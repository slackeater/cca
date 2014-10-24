from django.db import models
from datetime import datetime

# Create your models here.

class Upload(models.Model):
	fileName = models.CharField(max_length=256)
	uploadDate = models.DateTimeField(default=datetime.now, blank=True)
	uploadIP = models.IPAddressField(default="0.0.0.0",blank=True)
	parsed = models.BooleanField(default=False)
