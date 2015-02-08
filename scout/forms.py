from django import forms
from course.models import CourseInstance

class EditClassesForm(forms.Form):
	session = forms.ModelChoiceField(queryset=CourseInstance.objects.all())
