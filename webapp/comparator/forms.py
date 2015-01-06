from django import forms
from webapp import constConfig

class VerifyForm(forms.Form):
	""" This class represents the form used to display the verification types """

	verificationType = forms.ChoiceField(label="Verification Type",required=True,
			widget=forms.RadioSelect, choices=constConfig.VERIFY_CHOICES)

