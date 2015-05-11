from django import forms
from django.shortcuts import render, redirect
from django.core.context_processors import csrf
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.template import RequestContext
from django.views.decorators.http import require_http_methods
from mbu.forms import EditProfileForm, MbuUserCreationForm
from mbu.models import *
from mbu.scout_forms import EditClassesForm
import logging

logger = logging.getLogger(__name__)

def signup(request):
    form = MbuUserCreationForm()
    if request.POST:
        form = MbuUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('mbu_home')
    args = {'form' : form}
    return render(request, 'mbu/signup.html', args)

def login(request):
    args = {}
    form = AuthenticationForm()
    next = request.POST.get('next',request.GET.get('next','/'))
    print("Booya!")
    print(next)
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect(next)
        messages.add_message(request, messages.ERROR, 'Invalid username or password')
    args.update({'form':form})
    args.update({'next':next})
    return render(request, 'login.html', args)

def logout_user(request):
    logout(request)
    return redirect('mbu_home')

@login_required()
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

# Create your views here.
@permission_required('mbu.edit_scout_schedule',raise_exception=True)
def edit_classes(request):
    args = {}
    user = request.user
    form = EditClassesForm(user=user)
    if request.POST:
        form = EditClassesForm(request.POST, user=user)
        if form.is_valid():
            user.enrollments.clear()
            for name, course_instance in form.cleaned_data.items():
                if course_instance is not None:
                    user.enrollments.add(course_instance)
            user.save()
            messages.add_message(request, messages.SUCCESS, 'Your schedule has been updated.')
            return redirect('mbu_home')

    args.update({'form': form})
    args.update(csrf(request))
    return render(request, 'mbu/edit_classes.html', args)

def view_registered_classes(request):
    args = {}
    user = request.user
    enrolled_courses = user.enrollments.all()
    args.update({'enrolled_courses': enrolled_courses})
    return render(request, 'mbu/view_classes.html', args)

def view_troop_enrollees(request):
    args = {}
    scoutmaster = Scoutmaster.objects.get(user=request.user)
    troop = Troop.objects.get(scoutmaster=scoutmaster)
    scouts = Scout.objects.all().filter(troop=troop)
    args.update({'scouts': scouts})
    return render(request, 'scoutmaster/view_troop.html', args)

def view_troop_classes(request, scout_id):
    args = {}
    course_enrollments = Scout.objects.get(pk=scout_id).user.enrollments.all()
    args.update({'course_enrollments': course_enrollments})
    print (course_enrollments)
    return render(request, 'scoutmaster/view_troop_courses.html', args)
