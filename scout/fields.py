from django.forms import ModelChoiceField
from course.models import CourseInstance
from django.core.exceptions import ValidationError

class CourseInstanceChoiceField(ModelChoiceField):
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        session = kwargs.pop('session', None)
        queryset = CourseInstance.objects.filter(session=session)
        initial = user.enrollments.filter(session=session).first()
        super(CourseInstanceChoiceField, self).__init__(queryset=queryset, label=session.name, required=False, initial=initial)

    def clean(self, value):
        value = super(CourseInstanceChoiceField, self).clean(value)
        if value is not None and value.enrollees.count() >= value.max_enrollees:
            raise ValidationError("This course is full.", code="course_full")
        return value
