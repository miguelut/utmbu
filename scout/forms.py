from django import forms
from django.contrib.auth.models import User
from course.models import CourseInstance, Session
from mbu.models import MeritBadgeUniversity

class EditClassesForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super(EditClassesForm, self).__init__(*args, **kwargs)
        mbu = MeritBadgeUniversity.objects.filter(current=True)
        sessions = Session.objects.filter(mbu=mbu)
        for session in sessions:
            queryset = CourseInstance.objects.filter(session=session)
            self.fields['class-for-session-%d' % session.pk] = forms.ModelChoiceField(queryset=queryset, label=session.name)

