from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.context_processors import csrf
from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType
from scout.models import Scout 
from scoutmaster.models import Scoutmaster
from django.contrib import messages
from registration.forms import *
from mbu_users.models import Venture, Volunteer, TroopContact

# Create your views here.

def register_scout(request):
    args = {'title': 'Register Scout'}
    ct = ContentType.objects.get_for_model(Scout)
    p = Permission.objects.get(content_type=ct, codename='edit_scout_schedule')
    args.update({'perms':p})
    FormSet = ScoutFormSet
    return _register(request, FormSet, args)

def register_scoutmaster(request):
    args = {'title': 'Register Scoutmaster'}
    ct = ContentType.objects.get_for_model(Scoutmaster)
    p = Permission.objects.get(content_type=ct, codename='can_modify_troop_enrollments')
    args.update({'perms':p})
    FormSet = ScoutmasterFormSet
    return _register(request, FormSet, args)

def _register(request, FormSet, args):
    user = User()
    form = MbuUserCreationForm()
    formset = FormSet()
    if request.POST:
        form = MbuUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            formset = FormSet(request.POST, instance=user)
            if formset.is_valid():
                user.save()
                formset.save()
                perms = args.get('perms', None)
                if perms is not None:
                    user.user_permissions.add(perms)
                messages.add_message(request, messages.SUCCESS, 'Registration complete.  Please log in.')
                return HttpResponseRedirect('/login')                

    args.update(csrf(request))
    args.update({'form' : form })
    args.update({'formset': formset })  
    return render(request, 'registration/register_user.html', args)

def register(request):
    return render(request, 'registration/register.html')

def register_venture(request):
    args = {'title': 'Register Venture'}
    ct = ContentType.objects.get_for_model(Venture)
    #p = Permission.objects.get(content_type=ct, codename='can_modify_venture_enrollments')
    #args.update({'perms':p})
    FormSet = VentureFormSet
    return _register(request, FormSet, args)

def register_troopcontact(request):
    args = {'title': 'Register TroopContact'}
    ct = ContentType.objects.get_for_model(TroopContact)
    FormSet = TroopContactFormSet
    return _register(request, FormSet, args)

def register_volunteer(request):
    args = {'title': 'Register Volunteer'}
    ct = ContentType.objects.get_for_model(Volunteer)
    FormSet = VolunteerFormSet
    return _register(request, FormSet, args)
