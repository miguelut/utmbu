from django.forms import ModelForm
from django.contrib.auth.models import User
from mbu.models import Scout
from crispy_forms.helper import FormHelper
from django.forms.extras.widgets import SelectDateWidget


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

    class Meta:
        model = Scout
        fields = ['dob', 'rank', 'troop']
        widgets = {'dob': SelectDateWidget(years=range(2015, 1950, -1))}