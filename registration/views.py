from django.shortcuts import render, render_to_response
from django.core.context_processors import csrf
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from scout.models import Scout
from django.forms.models import inlineformset_factory

# Create your views here.

def register_scout(request):
    if request.POST:
        pass
    args = {}
    ScoutFormSet = inlineformset_factory(User, Scout, can_delete=False)
    user = User()
    form = UserCreationForm()
    formset = ScoutFormSet(instance=user)
    args.update(csrf(request))
    args.update({'form' : form })
    args.update({'formset': formset })    
    return render_to_response('registration/register_scout.html', args)

def register_scoutmaster(request):
    pass
