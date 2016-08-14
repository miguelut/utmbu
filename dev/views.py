from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Permission
from django.contrib.auth.hashers import make_password
from django.contrib.contenttypes.models import ContentType
from mbu.models import *
from datetime import date, datetime
import os

# Create your views here.
def setup_data(request):
    councils = create_councils()
    troop, create = Troop.objects.get_or_create(number=int('464'), council=councils[0])
    mbu, create = MeritBadgeUniversity.objects.get_or_create(name='MBU 2015', year=date.today(), current=True)
    timeblocks = create_timeblocks(mbu)
    courses = seed_courses()
    course_instances = create_course_instances(courses, timeblocks)
    user1, create = User.objects.get_or_create(first_name='First1', last_name='Last1', email="test1@test.com", username='test1', password=make_password('test1'))
    user2, create = User.objects.get_or_create(first_name='First2', last_name='Last2', email="test2@test.com", username='test2', password=make_password('test2'))
    ct = ContentType.objects.get_for_model(Scout)
    p = Permission.objects.get(content_type=ct, codename='edit_scout_schedule')
    user1.user_permissions.add(p)
    user2.user_permissions.add(p)
    scout1, create = Scout.objects.get_or_create(user=user1, rank='Star', troop=troop, waiver=False)
    scout2, create = Scout.objects.get_or_create(user=user2, rank='Star', troop=troop, waiver=False)
    return redirect('mbu_home')

def seed_courses():
    result = []
    files = os.listdir('./static/images/badges')
    for file in files:
        name = file.replace('_',' ').replace('.jpg', '')
        course, create = Course.objects.get_or_create(name=name, image_name=file)
        result.append(course)

    return result

def create_timeblocks(mbu):
    result = []
    timeblock1, create = TimeBlock.objects.get_or_create(name='Session 1', start_time=datetime(2015,2,14,8,0,0), end_time=datetime(2015,2,14,10,0,0), mbu=mbu)
    timeblock2, create = TimeBlock.objects.get_or_create(name='Session 2', start_time=datetime(2015,2,14,10,0,0), end_time=datetime(2015,2,14,12,0,0), mbu=mbu)
    timeblock3, create = TimeBlock.objects.get_or_create(name='Session 3', start_time=datetime(2015,2,14,13,0,0), end_time=datetime(2015,2,14,15,0,0), mbu=mbu)
    timeblock4, create = TimeBlock.objects.get_or_create(name='Session 4', start_time=datetime(2015,2,14,15,0,0), end_time=datetime(2015,2,14,17,0,0), mbu=mbu)
    result.append(timeblock1)
    result.append(timeblock2)
    result.append(timeblock3)
    result.append(timeblock4)
    return result

def create_course_instances(courses, timeblocks):
    result = []
    mod = len(timeblocks)
    for idx, val in enumerate(courses):
        timeblock = timeblocks[idx % mod]
        course_instance, create = ScoutCourseInstance.objects.get_or_create(course=val, timeblock=timeblock, location='Room %s' % str(idx), max_enrollees=10)
        result.append(course_instance)
    return result

def create_councils():
    result = []
    with open('./dev/councils.csv', 'r') as lines:
        for line in lines:
            number, name, city, state = line.strip().split(',')
            council, create = Council.objects.get_or_create(number=int(number), name=name, city=city, state=state)
            result.append(council)

    return result