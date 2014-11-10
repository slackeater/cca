from django.db import models
from django.utils import timezone
# Create your models here.

class Downloads(models.Model):
	""" A model to keep track of downloads """

	dirName = models.CharField(max_length=255)
	downTime = models.DateTimeField(default=timezone.now)
	status = models.IntegerField(max_length=1)
