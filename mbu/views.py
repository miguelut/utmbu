from django.shortcuts import render, render_to_response
from django.core.context_processors import csrf
from django.contrib.auth import authenticate, login

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

	return render_to_response('home.html')