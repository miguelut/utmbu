from django.shortcuts import render, render_to_response
from django.core.context_processors import csrf
from mbu.forms import EditProfileForm
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django import forms
from django.template import RequestContext
from mbu.models import Scout, User
import logging

logger = logging.getLogger(__name__)
args = {}
args.update({'links': [
    {'href':'mbu_home', 'label':'Home'}, 
    {'href':'edit_profile', 'label':'Edit Profile'},
    {'href':'class_schedule', 'label':'Class Schedule'},
    {'href':'reports', 'label':'Reports'},
    {'href':'class_list', 'label':'Class List'}
]})

def logout_user(request):
    logout(request)
    return redirect('mbu_home')

def view_home_page(request):
    context = RequestContext(request)
    return render_to_response('mbu/home.html', args, context_instance=context)

class RegisterScoutForm(forms.Form):
    username = forms.CharField(label='Username')
    password = forms.CharField(label='Password',widget=forms.PasswordInput)
    dob = forms.DateField(label='Date of Birth')
    rank = forms.CharField(label='Rank', max_length=15)
    troop = forms.CharField(label='Troop', max_length=15)

def register_scout(request):
    args.update({'form':RegisterScoutForm()})
    if request.POST:
        user = User()
        user.username = request.POST.get('username')
        user.password = request.POST.get('password')
        user.save()
    return render_to_response('mbu/register_scout.html', args)

def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST)
        if form.is_valid():
            # Process form if valid
            pass
    else:
        form = EditProfileForm()
        args.update({'form': form})
    
    return render(request, 'mbu/edit_profile.html', args)

def view_scoutmaster_page(request):
    # Set session info?
    return render_to_response('mbu/scoutmaster.html', args)

def view_class_list(request):
	args = {}
	args.update(csrf(request))
	classList = [];
	getClasslist(classList)
	args.update({ 'classlist': classList })
	return render_to_response('classlist.html', args)

def getClasslist(classList):
    # add timeslot info
    classList.append({'id': 1,
        'name': 'class1',
        'time': '9:00-10:30',
        'location': 'location1',
        'teacher': 'teacher1',
        'link': 'class_requirements'})
    classList.append({'id': 2,
        'name': 'class2',
        'time': '9:00-10:30',
        'location': 'location2',
        'teacher': 'teacher2',
        'link': 'class_requirements'})
    classList.append({'id': 3,
        'name': 'class3',
        'time': '9:00-10:30',
        'location': 'location3',
        'teacher': 'teacher3',
        'link': 'class_requirements'})
    return

def view_class_requirements(request, id=-1):
	args = {}
	args.update(csrf(request))
	#if (id < 0):
		#handle error
	args.update({'id': id})
	return render_to_response('classrequirements.html', args)

def view_class_schedule(request):
    return render_to_response('class_schedule.html', args)

def view_reports(request):
    return render_to_response('reports.html', args)