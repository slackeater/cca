from django import forms
from dashboard.models import MimeType
RES_CHOICES = ((0,'Deleted File'),(1,'MIME Type'),(2,'All'))

class MetaSearch(forms.Form):
	resType = forms.MultipleChoiceField(choices=RES_CHOICES, label="Research Type", required=True)

	# Get all MIME Type
	mimes = MimeType.objects.all().order_by('mime')
	mimesList = list()
	
	for m in mimes:
		mimesList.append((m.id,m.mime))

	mimeType = forms.ChoiceField(choices=mimesList, label="MIME Type")
