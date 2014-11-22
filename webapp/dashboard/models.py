from django.db import models
from django.utils import timezone

# Create your models here.

class MimeType(models.Model):
	""" A model for storing MIME types """
	mime = models.CharField(max_length=100)
