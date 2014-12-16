from django import forms
# Create your views here.

VERIFY_CHOICES = ((1,"Metadata"),(2,"Files"),(3,"Files+History (it can take a lot of time)"))

class VerifyForm(forms.Form):
	verificationType = forms.ChoiceField(label="Verification Type",required=True,
			widget=forms.RadioSelect, choices=VERIFY_CHOICES)

