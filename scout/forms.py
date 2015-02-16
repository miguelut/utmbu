from django import forms
from django.contrib.auth.models import User
from course.models import CourseInstance, Session
from mbu.models import MeritBadgeUniversity
from django.core.exceptions import ValidationError

class EditClassesForm(forms.Form):

    def __init__(self, *args, **kwargs):
        # Need to pop this guy before super()
        self.user = kwargs.pop('user', None)
        super(EditClassesForm, self).__init__(*args, **kwargs)
        sessions = self._get_sessions()
        for session in sessions:
            queryset = CourseInstance.objects.filter(session=session)
            initial = self.user.enrollments.filter(session=session).first()
            self.fields['class-for-session-%d' % session.pk] = forms.ModelChoiceField(queryset=queryset, label=session.name, required=False, initial=initial)
    
    # This is where we do cross-field validation
    def clean(self):
        cleaned_data = super(EditClassesForm, self).clean()
        
        overlapping_sessions = self._get_overlapping_sessions()
        chosen_sessions = set()
        for k in cleaned_data:
            chosen_sessions.add(cleaned_data[k])
            
        for s1, s2 in overlapping_sessions:
            if s1 in chosen_sessions and s2 in chosen_sessions:
                raise ValidationError("Cannot enroll in both '%s' and '%s': they are at the same time." % (s1, s2))

        return cleaned_data

    # Return a list of all pairs of overlapping sessions
    def _get_overlapping_sessions(self):
        sessions = self._get_sessions()
        overlapping_sessions = set()
        for session1 in sessions:
            for session2 in sessions:
                if session1 != session2:
                    if self._sessions_overlap(session1, session2):
                        overlapping_sessions.add((session1.pk, session2.pk))
        return overlapping_sessions

    def _get_sessions(self):
        mbu = MeritBadgeUniversity.objects.filter(current=True)
        sessions = Session.objects.filter(mbu=mbu)
        return sessions

    def _sessions_overlap(self, session1, session2):
        no_overlap = session1.start_time < session2.start_time and session1.end_time <= session2.end_time \
                  or session1.start_time >= session2.end_time and session1.end_time > session2.end_time
        return not no_overlap
