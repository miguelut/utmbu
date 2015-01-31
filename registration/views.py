from django.shortcuts import render, render_to_response
from django.http import HttpResponseRedirect
from django.core.context_processors import csrf
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from scout.models import Scout
from django.contrib import messages
from registration.forms import ScoutFormSet

# Create your views here.

def register_scout(request):
    args = {}
    user = User()
    form = UserCreationForm()
    formset = ScoutFormSet()
    if request.POST:
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            scout_formset = ScoutFormSet(request.POST, instance=user)
            if scout_formset.is_valid():
                user.save()
                scout_formset.save()
                messages.add_message(request, messages.SUCCESS, 'Registration complete.  Please log in.')
                return HttpResponseRedirect('/login')                

    args.update(csrf(request))
    args.update({'form' : form })
    args.update({'formset': formset })    
    return render_to_response('registration/register_scout.html', args)

def register_scoutmaster(request):
    pass
