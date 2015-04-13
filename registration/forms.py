from django import forms
from django.contrib.auth.models import User
from django.forms.models import inlineformset_factory
from django.forms.extras.widgets import SelectDateWidget
from django.contrib.auth.forms import UserCreationForm
from scout.models import Scout, Parent
from scoutmaster.models import Scoutmaster
from troop.models import Troop, Council
from mbu_users.models import Venture, Volunteer, TroopContact
from django.forms import ModelForm
from troop.models import Troop, Council


ScoutFormSet = inlineformset_factory(User, Scout, can_delete=False, widgets={'dob': SelectDateWidget()}, exclude = ['parent'])
ScoutmasterFormSet = inlineformset_factory(User, Scoutmaster, can_delete=False, fields='__all__')
ParentFormSet =inlineformset_factory(User, Parent, can_delete=False, widgets={'dob': SelectDateWidget()}, fields='__all__')
VentureFormSet = inlineformset_factory(User, Venture, can_delete=False, fields='__all__')
VolunteerFormSet = inlineformset_factory(User, Volunteer, can_delete=False, fields='__all__')
TroopContactFormSet = inlineformset_factory(User, TroopContact, can_delete=False, fields='__all__')
TroopFormSet = inlineformset_factory(Council, Troop, can_delete=False, fields='__all__')

class MbuUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField()

    def save(self, commit=True):
        user = super(MbuUserCreationForm, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
        
    class Meta:
        model = User
        fields = ['first_name','last_name','email','username']

class TroopForm(forms.ModelForm):
    class Meta:
        model = Troop
        fields = '__all__'

class CouncilForm(forms.ModelForm):
    not_present = forms.BooleanField(label='New Council', widget=forms.CheckboxInput(attrs={'onClick':'alert("Hello!")'}))
    name = forms.CharField(max_length=30, widget=forms.HiddenInput())

    class Meta:
        model = Council
        fields = '__all__'
