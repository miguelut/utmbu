from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from mbu.models import Scout, Scoutmaster, Parent
from crispy_forms.helper import FormHelper


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


class UserProfileForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class ScoutProfileForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ScoutProfileForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        if 'instance' in kwargs:
            if kwargs['instance'].troop is not None:
                if 'troop' in self.fields:
                    del self.fields['troop']

    class Meta:
        model = Scout
        exclude = ['user', 'waiver', 'parent']


class ScoutmasterProfileForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ScoutmasterProfileForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        if 'instance' in kwargs:
            if kwargs['instance'].troop is not None:
                if 'troop' in self.fields:
                    del self.fields['troop']

    class Meta:
        model = Scoutmaster
        exclude = ['user']


class ParentProfileForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ParentProfileForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        if 'instance' in kwargs:
            if kwargs['instance'].troop is not None:
                if 'troop' in self.fields:
                    del self.fields['troop']

    class Meta:
        model = Parent
        exclude = ['user']
