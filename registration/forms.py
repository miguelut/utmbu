from django import forms
from django.contrib.auth.models import User
from django.forms.models import inlineformset_factory
from django.forms.extras.widgets import SelectDateWidget
from django.contrib.auth.forms import UserCreationForm
from scout.models import Scout


ScoutFormSet = inlineformset_factory(User, Scout, can_delete=False, widgets={'dob': SelectDateWidget()})

class ScoutUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField()

    def save(self, commit=True):
        user = super(ScoutUserCreationForm, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
        
    
    class Meta:
        model = User
        fields = ['first_name','last_name','email','username']
