from django.shortcuts import render, render_to_response
from django.core.context_processors import csrf
from django.contrib.auth import authenticate, login
from django import forms
from mbu.models import Scout, User

# Create your views here.
def login_user(request):
    args = {}
    args.update(csrf(request))
    message = "Please log in below..."
    username_given = ''
    password_given = ''
    if request.POST:
        username_given = request.POST.get('username')
        password_given = request.POST.get('password')

        user = authenticate(username=username_given, password=password_given)
        if user is not None:
            if user.is_active:
                login(request, user)
                message = "You're logged in!"
            else:
                message = "Youraccount exists, but is not active."
        else:
            message= "Your username/password combination was invalid..."

    args.update({'message': message})
    args.update({'username': username_given})
    return render_to_response('login.html', args)

def home(request):
    args = {}
    args.update(csrf(request))
    args.update({'links': [{'href':'mbu_home', 'label':'Home'}]})
    return render_to_response('mbu/home.html', args)

class RegisterScoutForm(forms.Form):
    username = forms.CharField(label='Username')
    password = forms.CharField(label='Password',widget=forms.PasswordInput)
    dob = forms.DateField(label='Date of Birth')
    rank = forms.CharField(label='Rank', max_length=15)
    troop = forms.CharField(label='Troop', max_length=15)

def register_scout(request):
    args = {}
    args.update(csrf(request))
    args.update({'form':RegisterScoutForm()})
    if request.POST:
        user = User()
        user.username = request.POST.get('username')
        user.password = request.POST.get('password')
        user.save()

    return render_to_response('mbu/register_scout.html',args)
        # if validation
          # save user
          # save scout
          # redirect login

def scoutmaster(request):
    args = {}
    args.update(csrf(request))
    args.update({'links':[{'href':'mbu_home', 'label':'Home'}]})
    # Set session info?
    return render_to_response('mbu/scoutmaster.html',args)
