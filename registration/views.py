from django.shortcuts import render, render_to_response

# Create your views here.

def register_scout(request):
    return render_to_response('registration/register_scout.html')

def register_scoutmaster(request):
    pass
