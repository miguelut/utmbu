from django.shortcuts import render, render_to_response
from django.http import HttpResponseRedirect
from django.core.context_processors import csrf
from django.contrib.auth.models import User
from scout.models import Scout
from django.contrib import messages
from registration.forms import ScoutFormSet, ScoutmasterFormSet, MbuUserCreationForm

# Create your views here.

def register_scout(request):
    args = {'title': 'Register Scout'}
    FormSet = ScoutFormSet
    return _register(request, FormSet, args)

def register_scoutmaster(request):
    args = {'title': 'Register Scoutmaster'}
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
                messages.add_message(request, messages.SUCCESS, 'Registration complete.  Please log in.')
                return HttpResponseRedirect('/login')                

    args.update(csrf(request))
    args.update({'form' : form })
    args.update({'formset': formset })  
    return render_to_response('registration/register.html', args)
