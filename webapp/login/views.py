from django.shortcuts import render
from django import forms
from django.http import HttpResponse
from login import models

# Create your views here.

class UserForm(forms.ModelForm):
	class Meta:
		model = models.Login
		fields = ['uname','password']
		widgets = {
				'password': forms.PasswordInput(),
		}

def index(request):
	
	if request.method == "POST":
		# process password and username
		form = "Submitted"
		print "Submitted"
	else:	
		form = UserForm()

	return render(request, 'index.html', {'form': form})
