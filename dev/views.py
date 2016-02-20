from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Permission
from django.contrib.auth.hashers import make_password
from django.contrib.contenttypes.models import ContentType
from mbu.models import *
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
    session1, create = TimeBlock.objects.get_or_create(name='Session 1', start_time=datetime(2015,2,14,8,0,0), end_time=datetime(2015,2,14,10,0,0), mbu=mbu)
    session2, create = TimeBlock.objects.get_or_create(name='Session 2', start_time=datetime(2015,2,14,10,0,0), end_time=datetime(2015,2,14,12,0,0), mbu=mbu)
    session3, create = TimeBlock.objects.get_or_create(name='Session 3', start_time=datetime(2015,2,14,13,0,0), end_time=datetime(2015,2,14,15,0,0), mbu=mbu)
    session4, create = TimeBlock.objects.get_or_create(name='Session 4', start_time=datetime(2015,2,14,15,0,0), end_time=datetime(2015,2,14,17,0,0), mbu=mbu)
    course_instance1, create = ScoutCourseInstance.objects.get_or_create(course=course1, session=session1, location='Room 1', max_enrollees=0)
    course_instance2, create = ScoutCourseInstance.objects.get_or_create(course=course1, session=session2, location='Room 7', max_enrollees=10)
    course_instance3, create = ScoutCourseInstance.objects.get_or_create(course=course1, session=session4, location='Room 8', max_enrollees=10)
    course_instance4, create = ScoutCourseInstance.objects.get_or_create(course=course2, session=session1, location='Room 2', max_enrollees=10)
    course_instance5, create = ScoutCourseInstance.objects.get_or_create(course=course2, session=session3, location='Room 3', max_enrollees=10)
    course_instance6, create = ScoutCourseInstance.objects.get_or_create(course=course3, session=session2, location='Room 4', max_enrollees=10)
    course_instance7, create = ScoutCourseInstance.objects.get_or_create(course=course3, session=session3, location='Room 5', max_enrollees=10)
    course_instance8, create = ScoutCourseInstance.objects.get_or_create(course=course3, session=session4, location='Room 6', max_enrollees=10)
    user1, create = User.objects.get_or_create(first_name='First1', last_name='Last1', email="test1@test.com", username='test1', password=make_password('test1'))
    user2, create = User.objects.get_or_create(first_name='First2', last_name='Last2', email="test2@test.com", username='test2', password=make_password('test2'))
    ct = ContentType.objects.get_for_model(Scout)
    p = Permission.objects.get(content_type=ct, codename='edit_scout_schedule')
    user1.user_permissions.add(p)
    user2.user_permissions.add(p)
    scout1, create = Scout.objects.get_or_create(user=user1, dob=date(2000,1,1), rank='Star', troop=troop)
    scout2, create = Scout.objects.get_or_create(user=user2, dob=date(2000, 2, 2), rank='Star', troop=troop)
    return redirect('mbu_home')
