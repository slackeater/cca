from django import forms

class CloudItemForm(forms.Form):
	name = forms.CharField(label="Name")
	description = forms.CharField(label="Description",widget=forms.Textarea)

