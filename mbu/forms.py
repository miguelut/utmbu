from django.forms import ModelForm
from django.contrib.auth.models import User
from django.forms.models import inlineformset_factory
from django.forms.extras.widgets import SelectDateWidget
from mbu.models import Scout
from crispy_forms.helper import FormHelper


class UserProfileForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

ScoutFormSet = inlineformset_factory(User, Scout, can_delete=False, widgets={'dob': SelectDateWidget(years=range(2015, 1950, -1))}, fields='__all__')