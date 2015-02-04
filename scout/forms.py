from django import forms
from course.models import Session, Course

class EditClassesForm(forms.Form):
	session = forms.ModelChoiceField(queryset=Session.objects.all(), initial={'pk': 1})