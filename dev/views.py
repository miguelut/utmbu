from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Permission
from django.contrib.auth.hashers import make_password
from django.contrib.contenttypes.models import ContentType
from mbu.models import *
from datetime import date, datetime
import os


# Create your views here.
def setup_data(request):
    insert_courses()
    # councils = create_councils()
    # troop, create = Troop.objects.get_or_create(number=int('464'), council=councils[0])
    # mbu, create = MeritBadgeUniversity.objects.get_or_create(name='MBU 2015', year=date.today(), current=True)
    # timeblocks = create_timeblocks(mbu)
    # courses = seed_courses()
    # course_instances = create_course_instances(courses, timeblocks)
    # user1, create = User.objects.get_or_create(first_name='First1', last_name='Last1', email="test1@test.com", username='test1', password=make_password('test1'))
    # user2, create = User.objects.get_or_create(first_name='First2', last_name='Last2', email="test2@test.com", username='test2', password=make_password('test2'))
    # ct = ContentType.objects.get_for_model(Scout)
    # p = Permission.objects.get(content_type=ct, codename='edit_scout_schedule')
    # user1.user_permissions.add(p)
    # user2.user_permissions.add(p)
    # scout1, create = Scout.objects.get_or_create(user=user1, rank='Star', troop=troop, waiver=False)
    # scout2, create = Scout.objects.get_or_create(user=user2, rank='Star', troop=troop, waiver=False)
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
    timeblock5, create = TimeBlock.objects.get_or_create(name='Session 1-Double', start_time=datetime(2015,2,14,8,0,0), end_time=datetime(2015,2,14,12,0,0), mbu=mbu, double=True)
    timeblock6, create = TimeBlock.objects.get_or_create(name='Session 3-Double', start_time=datetime(2015,2,14,13,0,0), end_time=datetime(2015,2,14,17,0,0), mbu=mbu, double=True)
    result.append(timeblock1)
    result.append(timeblock2)
    result.append(timeblock3)
    result.append(timeblock4)
    result.append(timeblock5)
    result.append(timeblock6)
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


def insert_courses():
    assignments = [
    ("American Business", 1),
        ("American Cultures", 2),
        ("American Labor", 3),
        ("Animation", 1),
        ("Animation", 2),
        ("Animation", 3),
        ("Animation", 4),
        ("Architecture", 5),
        ("Architecture", 6),
        ("Archaeology", 3),
        ("Art", 1),
        ("Art", 2),
        ("Art", 3),
        ("Art", 4),
        ("Aviation", 1),
        ("Aviation", 2),
        ("Chess", 1),
        ("Chess", 2),
        ("Chess", 3),
        ("Chess", 4),
        ("Chemistry", 1),
        ("Chemistry", 2),
        ("Chemistry", 3),
        ("Chemistry", 4),
        ("Citizenship in the Community", 1),
        ("Citizenship in the Community", 2),
        ("Citizenship in the Community", 3),
        ("Citizenship in the Community", 4),
        ("Citizenship in the Community", 1),
        ("Citizenship in the Community", 2),
        ("Citizenship in the Community", 3),
        ("Citizenship in the Community", 4),
        ("Citizenship in the Nation", 5),
        ("Citizenship in the Nation", 6),
        ("Citizenship in the Nation", 5),
        ("Citizenship in the Nation", 6),
        ("Citizenship in the World", 1),
        ("Citizenship in the World", 2),
        ("Citizenship in the World", 3),
        ("Citizenship in the World", 4),
        ("Citizenship in the World", 1),
        ("Citizenship in the World", 2),
        ("Citizenship in the World", 3),
        ("Communication", 1),
        ("Communication", 2),
        ("Communication", 3),
        ("Communication", 4),
        ("Communication", 1),
        ("Communication", 2),
        ("Communication", 3),
        ("Communication", 4),
        ("Cooking", 1),
        ("Cooking", 2),
        ("Cooking", 3),
        ("Cooking", 4),
        ("Cooking", 1),
        ("Cooking", 2),
        ("Cooking", 3),
        ("Cooking", 4),
        ("Crime Prevention", 3),
        ("Crime Prevention", 4),
        ("Emergency Preparedness", 1),
        ("Emergency Preparedness", 2),
        ("Emergency Preparedness", 3),
        ("Emergency Preparedness", 4),
        ("Energy", 1),
        ("Energy", 2),
        ("Engineering", 5),
        ("Engineering", 6),
        ("Family Life", 1),
        ("Family Life", 2),
        ("Family Life", 3),
        ("Family Life", 4),
        ("Family Life", 1),
        ("Family Life", 2),
        ("Family Life", 3),
        ("Family Life", 4),
        ("Fingerprinting", 1),
        ("Fingerprinting", 2),
        ("Fingerprinting", 3),
        ("Fingerprinting", 4),
        ("Fire Safety", 3),
        ("Fire Safety", 4),
        ("First Aid", 5),
        ("First Aid", 6),
        ("First Aid", 5),
        ("First Aid", 6),
        ("Geology", 4),
        ("Inventing", 1),
        ("Law", 2),
        ("Medicine", 5),
        ("Moviemaking", 1),
        ("Moviemaking", 2),
        ("Moviemaking", 3),
        ("Moviemaking", 4),
        ("Music", 1),
        ("Music", 2),
        ("Music", 3),
        ("Music", 4),
        ("Nuclear Science", 5),
        ("Nuclear Science", 6),
        ("Painting", 1),
        ("Painting", 2),
        ("Personal Fitness", 1),
        ("Personal Fitness", 2),
        ("Personal Fitness", 3),
        ("Personal Fitness", 4),
        ("Personal Management", 1),
        ("Personal Management", 2),
        ("Personal Management", 3),
        ("Personal Management", 4),
        ("Personal Management", 1),
        ("Personal Management", 2),
        ("Personal Management", 3),
        ("Personal Management", 4),
        ("Photography", 3),
        ("Photography", 4),
        ("Public Health", 3),
        ("Public Speaking", 4),
        ("Radio", 5),
        ("Radio", 6),
        ("Safety", 1),
        ("Salesmanship", 2),
        ("Scholarship", 3),
        ("Sculpture", 1),
        ("Sculpture", 2),
        ("Sculpture", 3),
        ("Sculpture", 4),
        ("Space Exploration", 3),
        ("Space Exploration", 4),
        ("Sports", 1),
        ("Sports", 2),
        ("Surveying", 5),
        ("Veterinary Medicine", 1),
        ("Veterinary Medicine", 2),
        ("Weather", 4)
    ]

    for name, id in assignments:
        max = 20
        try:
            badge = Course.objects.get(name=name)
            timeblock = TimeBlock.objects.get(pk=id)
            ScoutCourseInstance.objects.create(course=badge, timeblock=timeblock, max_enrollees=max)
        except Exception as e:
            print(name)
            print(e)