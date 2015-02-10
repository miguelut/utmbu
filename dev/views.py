from django.shortcuts import render, redirect
from troop.models import Troop, Council
from scout.models import Scout
from scoutmaster.models import Scoutmaster
from mbu.models import MeritBadgeUniversity
from course.models import Session, Course, CourseInstance
from datetime import date, datetime

# Create your views here.
def setup_dummy_data(request):
    council, create = Council.objects.get_or_create(name='Test Council')
    council.save()
    troop, create = Troop.objects.get_or_create(number='464', council=council)
    council.save()
    mbu, create = MeritBadgeUniversity.objects.get_or_create(name='MBU 2015', year=date.today(), current=True)
    course1, create = Course.objects.get_or_create(name='Test Course 1')
    course2, create = Course.objects.get_or_create(name='Test Course 2')
    course3, create = Course.objects.get_or_create(name='Test Course 3')
    session1, create = Session.objects.get_or_create(name='Session 1', start_time=datetime(2015,2,14,8,0,0), end_time=datetime(2015,2,14,10,0,0), mbu=mbu)
    session2, create = Session.objects.get_or_create(name='Session 2', start_time=datetime(2015,2,14,10,0,0), end_time=datetime(2015,2,14,12,0,0), mbu=mbu)
    session3, create = Session.objects.get_or_create(name='Session 3', start_time=datetime(2015,2,14,13,0,0), end_time=datetime(2015,2,14,15,0,0), mbu=mbu)
    session4, create = Session.objects.get_or_create(name='Session 4', start_time=datetime(2015,2,14,15,0,0), end_time=datetime(2015,2,14,17,0,0), mbu=mbu)
    course_instance1, create = CourseInstance.objects.get_or_create(course=course1, session=session1)
    course_instance2, create = CourseInstance.objects.get_or_create(course=course1, session=session2)
    course_instance3, create = CourseInstance.objects.get_or_create(course=course2, session=session1)
    course_instance4, create = CourseInstance.objects.get_or_create(course=course2, session=session3)
    course_instance5, create = CourseInstance.objects.get_or_create(course=course3, session=session2)
    course_instance6, create = CourseInstance.objects.get_or_create(course=course3, session=session3)
    return redirect('mbu_home')
