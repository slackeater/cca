from django import forms
from dashboard.models import MimeType
from datetime import date
from webapp import constConfig

class MetaSearch(forms.Form):
	""" This class represent the form for searchin through the metadata """

	formType = forms.ChoiceField(choices=constConfig.CS_FORM_TYPE, label="Type", required=True,widget=forms.RadioSelect)
	resType = forms.ChoiceField(choices=constConfig.CS_RES_CHOICES, label="Type", required=True,widget=forms.RadioSelect)

	# Get all MIME Type
	mimes = MimeType.objects.all().order_by('mime')
	mimesList = list()
	
	for m in mimes:
		mimesList.append((m.id,m.mime))

	mimeType = forms.ChoiceField(choices=mimesList, label="MIME Type",widget=forms.Select(attrs={'class':'form-control'}))

	startDateYear = date.today().year

	startDate = forms.DateField(initial="31/12/"+str(startDateYear-2),required=True,label="Start Date",input_formats=['%d/%m/%Y'],widget=forms.DateInput(format='%d/%m/%Y',attrs={'id':'dp1','class':'form-control'}))
	endDate = forms.DateField(initial="31/12/"+str(startDateYear),required=True,label="End Date",input_formats=['%d/%m/%Y'],widget=forms.DateInput(format='%d/%m/%Y',attrs={'id':'dp2','class':'form-control'}))

	email = forms.EmailField(label="E-Mail",required=False,widget=forms.TextInput(attrs={'class':'form-control'}))
	givenname = forms.CharField(label="Name",required=False,widget=forms.TextInput(attrs={'class':'form-control'}))
	filename = forms.CharField(label="File Name",required=False,widget=forms.TextInput(attrs={'class':'form-control'}))
