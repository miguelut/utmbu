from django.shortcuts import render
from django.core.context_processors import csrf
from mbu.forms import EditProfileForm
from mbu.models import MeritBadgeUniversity
from course.models import Session, CourseInstance, Course
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django import forms
from django.template import RequestContext
from scout.models import Scout
import logging

logger = logging.getLogger(__name__)

def logout_user(request):
    logout(request)
    return redirect('mbu_home')

def view_home_page(request):
    return render(request, 'mbu/home.html')

def edit_profile(request):
    args = {}
    if request.method == 'POST':
        form = EditProfileForm(request.POST)
        if form.is_valid():
            # Process form if valid
            pass
    else:
        form = EditProfileForm()
        args.update({'form': form})
    
    return render(request, 'mbu/edit_profile.html', args)

def view_class_list(request):
    args = {}
    args.update(csrf(request))
    mbu = MeritBadgeUniversity.objects.get(current=True)
    sessions = Session.objects.filter(mbu=mbu).values('pk')
    course_instances = CourseInstance.objects.filter(session__pk__in=sessions)
    args.update({ 'classlist': course_instances })
    return render(request, 'mbu/classlist.html', args)

def view_class_requirements(request, id=-1):
	args = {}
	args.update(csrf(request))
	#if (id < 0):
		#handle error
	args.update({'id': id})
	return render(request, 'mbu/classrequirements.html', args)

def view_reports(request):
    return render(request, 'mbu/reports.html')
