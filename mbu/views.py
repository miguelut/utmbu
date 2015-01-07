from django.shortcuts import render, render_to_response
from django.core.context_processors import csrf
from django.contrib.auth import authenticate, login
from mbu.forms import EditProfileForm

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
    return render_to_response('home.html', args)

def edit_profile(request):
    args = {
        'links': [
            {'href':'mbu_home', 'label':'Home'}
        ]}
    if request.method == 'POST':
        form = EditProfileForm(request.POST)
        if form.is_valid():
            # Process form if valid
            pass
    else:
        form = EditProfileForm()
        args.update({'form': form})
    
    return render(request, 'mbu/edit_profile.html', args)

def classlist(request):
    args = {}
    args.update(csrf(request))
    classList = [];
    getClasslist(classList)
    args.update({ 'classlist': classList })
    return render_to_response('classlist.html', args)


def getClasslist(classList):
    # add timeslot info
    classList.append({'id': 1, 'name': 'class1', 'location': 'location1', 'teacher': 'teacher1', 'link': 'class_requirements'})
    classList.append({'id': 2, 'name': 'class2', 'location': 'location2', 'teacher': 'teacher2', 'link': 'class_requirements'})
    classList.append({'id': 3, 'name': 'class3', 'location': 'location3', 'teacher': 'teacher3', 'link': 'class_requirements'})

    return

def classrequirements(request, id=-1):
    args = {}
    args.update(csrf(request))
    #if (id < 0):
        #handle error
    args.update({'id': id})
    return render_to_response('classrequirements.html', args)
