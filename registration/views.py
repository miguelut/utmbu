from django.shortcuts import render, render_to_response
from registration.forms import ScoutForm

# Create your views here.

def register_scout(request):
    args = {}
    args.update({'form': ScoutForm() })    
    return render_to_response('registration/register_scout.html', args)

def register_scoutmaster(request):
    pass
