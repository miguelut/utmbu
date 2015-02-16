from django.test import TestCase
from course.models import Session, CourseInstance, Course
from mbu.models import MeritBadgeUniversity
from scout.forms import EditClassesForm
from django.contrib.auth.models import User
from datetime import date, datetime
from django.core.exceptions import ValidationError

# Create your tests here.
class ScoutTestCase(TestCase):
    def setUp(self):
        self.mbu, create = MeritBadgeUniversity.objects.get_or_create(name='Test MBU', year=date.today(), current=True)
        self.c1, create = Course.objects.get_or_create(name='Test Course 1')
        self.c2, create = Course.objects.get_or_create(name='Test Course 2')
        self.c3, create = Course.objects.get_or_create(name='Test Course 3')
        self.s1, create = Session.objects.get_or_create(name='Session 1', start_time=datetime(2015,2,14,8,0,0), end_time=datetime(2015,2,14,10,0,0), mbu=self.mbu)
        self.s2, create = Session.objects.get_or_create(name='Session 2', start_time=datetime(2015,2,14,10,0,0), end_time=datetime(2015,2,14,12,0,0), mbu=self.mbu)
        self.s3, create = Session.objects.get_or_create(name='Session 3', start_time=datetime(2015,2,14,9,0,0), end_time=datetime(2015,2,14,12,0,0), mbu=self.mbu)
        self.c_i1, create = CourseInstance.objects.get_or_create(course=self.c1, session=self.s1, location='Room 1', max_enrollees=10)
        self.c_i2, create = CourseInstance.objects.get_or_create(course=self.c1, session=self.s2, location='Room 2', max_enrollees=10)
        self.c_i3, create = CourseInstance.objects.get_or_create(course=self.c1, session=self.s3, location='Room 3', max_enrollees=10)
        self.user, create = User.objects.get_or_create(username='michael', email='test@test.test', password='test')

    def test_session_overlap_causes_invalid_edit_classes_form(self):
        user = User.objects.get(username='michael')
        form = EditClassesForm(user=user)
        form.cleaned_data={'class-for-session-1':1, 'class-for-session-3':3}
        with self.assertRaises(ValidationError):
            form.clean()
        
    def test_session_non_overlap_does_not_raise_exception(self):
        user = User.objects.get(username='michael')
        form = EditClassesForm(user=user)
        form.cleaned_data={'class-for-session-1':1, 'class-for-session-2':2}
        form.clean()
        
        
