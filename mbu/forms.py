from django.forms import ModelForm, Form, CharField
from django.contrib.auth.models import User
from django.forms.models import inlineformset_factory
from django.forms.extras.widgets import SelectDateWidget
from mbu.models import Scout


class ScoutEditProfileForm(ModelForm):
    class Meta:
        model = Scout
        fields = '__all__'


class UserProfileForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

ScoutFormSet = inlineformset_factory(User, Scout, can_delete=False, widgets={'dob': SelectDateWidget(years=range(2015, 1950, -1))}, fields='__all__')