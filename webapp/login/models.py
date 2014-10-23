from django.db import models
from django import forms

# Create your models here.

class Login(models.Model):
	uname = models.CharField(max_length=10)
	password = models.CharField(max_length=256)

	def __str__(self):
		return self.uname

