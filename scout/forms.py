from django import forms
from django.contrib.auth.models import User
from course.models import CourseInstance, Session
from mbu.models import MeritBadgeUniversity

class EditClassesForm(forms.Form):

    def __init__(self, *args, **kwargs):
        # Need to pop this guy before super()
        user = kwargs.pop('user', None)
        super(EditClassesForm, self).__init__(*args, **kwargs)
        mbu = MeritBadgeUniversity.objects.filter(current=True)
        sessions = Session.objects.filter(mbu=mbu)
        for session in sessions:
            queryset = CourseInstance.objects.filter(session=session)
            initial = user.enrollments.filter(session=session).first()
            self.fields['class-for-session-%d' % session.pk] = forms.ModelChoiceField(queryset=queryset, label=session.name, required=False, initial=initial)
    
    def clean(self):
        cleaned_data = super(EditClassesForm, self).clean()

        return cleaned_data
