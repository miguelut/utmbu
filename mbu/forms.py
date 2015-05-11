from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.conf.global_settings import EMAIL_BACKEND

class EditProfileForm(forms.Form):
	first_name = forms.CharField(label='First Name')
	last_name = forms.CharField(label='Last Name')
	email = forms.CharField(label="Email")
	
class MbuUserCreationForm(UserCreationForm):
	"""
	A form that creates a user with username, first_name, last_name, 
	email, and password.  See UserCreationForm for more details.
	"""
	first_name = forms.CharField(required=True)
	last_name = forms.CharField(required=True)
	email = forms.EmailField(required=True)

	class Meta:
		model = User
		fields = ('username', 'first_name', 'last_name', 'email')
		
	def save(self, commit=True):
		user = super(MbuUserCreationForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		user.first_name = self.cleaned_data['first_name']
		user.last_name = self.cleaned_data['last_name']
		if commit:
			user.save()
		return user