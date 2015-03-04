from django import forms

class EditProfileForm(forms.Form):
	first_name = forms.CharField(label='First Name')
	last_name = forms.CharField(label='Last Name')
	email = forms.CharField(label="Email")