from django import forms
from models import MimeType
RES_CHOICES = ((0,'Deleted File'),(1,'MIME Type'),(2,'All'))

class DropMetaSearch(forms.Form):
	resType = forms.MultipleChoiceField(choices=RES_CHOICES, label="Research Type", required=True)

	# Get all MIME Type
	mimes = MimeType.objects.all()
	mimesList = list()
	for m in mimes:
		cleanMime = m.mime.strip("\n")
		mimesList.append((cleanMime,cleanMime))

	mimeType = forms.ChoiceField(choices=mimesList, label="MIME Type")
