import logging
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from django.core.context_processors import csrf
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import permission_required, user_passes_test
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import Permission, ContentType
from django.views.decorators.http import require_http_methods
from paypal.standard.forms import PayPalPaymentsForm
from django.http import HttpResponse
from mbu.forms import *
from mbu.models import *
from mbu.util import _is_user_scout, _is_user_scoutmaster, _populate_courses
from mbu.scout_forms import EditClassesForm
from utmbu import settings

logger = logging.getLogger(__name__)


def signup(request):
    """This is the default signup method.
    This method will register a user and a corresponding Scout."""
    form = MbuUserCreationForm()
    if request.POST:
        form = MbuUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Scout(user=user).save()
            ct = ContentType.objects.get(app_label='mbu', model='scout')
            perms = [
                Permission.objects.get(codename='edit_scout_schedule', content_type=ct),
                Permission.objects.get(codename='edit_scout_profile', content_type=ct)
            ]
            for perm in perms:
                user.user_permissions.add(perm)
            user.save()
            messages.add_message(request, messages.SUCCESS, 'Successfully registered.')
            return redirect('mbu_home')
    args = {'form': form}
    return render(request, 'mbu/signup.html', args)


def login(request):
    args = {}
    form = AuthenticationForm()
    next = request.POST.get('next', request.GET.get('next','/'))
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect(next)
        messages.add_message(request, messages.ERROR, 'Invalid username or password')
    args.update({'form':form})
    args.update({'next':next})
    return render(request, 'login.html', args)


def logout_user(request):
    logout(request)
    return redirect('mbu_home')


def view_home_page(request):
    if _is_user_scout(request.user):
        return _render_scout_homepage(request)
    elif _is_user_scoutmaster(request.user):
        return render(request, 'mbu/scoutmaster_home.html')
    return render(request, 'mbu/home.html')


def _render_scout_homepage(request):
    args = {'enrollments': request.user.enrollments.all()}
    return render(request, 'mbu/scout_home.html', args)


def register_user_as_scout(request):
    if not _is_user_scout(request.user) and not _is_user_scoutmaster(request.user):
        Scout(user=request.user).save()
        return redirect('edit_scout_profile')
    return redirect('mbu_home')


def register_user_as_scoutmaster(request):
    if not _is_user_scoutmaster(request.user) and not _is_user_scout(request.user):
        Scoutmaster(user=request.user).save()
        return redirect('edit_scoutmaster_profile')
    return redirect('mbu_home')


@user_passes_test(_is_user_scout, login_url='/login/')
def edit_scout_profile(request):
    args = {}
    scout_form = ScoutProfileForm
    scout = Scout(user=request.user)
    try:
        scout = Scout.objects.get(user=request.user)
    except Scout.DoesNotExist:
        pass

    return _edit_profile(request, scout_form, scout, args)


@user_passes_test(_is_user_scoutmaster, login_url='/login/')
def edit_scoutmaster_profile(request):
    args = {}
    scoutmaster_form = ScoutmasterProfileForm
    scoutmaster = Scoutmaster(user=request.user)
    try:
        scoutmaster = Scoutmaster.objects.get(user=request.user)
    except Scoutmaster.DoesNotExist:
        pass

    return _edit_profile(request, scoutmaster_form, scoutmaster, args)


def _edit_profile(request, ProfileForm, user, args):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=user)
        if form.is_valid() and profile_form.is_valid():
            form.save()
            profile_form.save()
            messages.add_message(request, messages.SUCCESS, 'Your profile has been saved.')
    else:
        form = UserProfileForm(instance=request.user)
        profile_form = ProfileForm(instance=user)
    args.update({'form': form})
    args.update({'profile_form': profile_form})
    
    return render(request, 'mbu/edit_profile.html', args)


def view_class_list(request):
    args = {}
    args.update(csrf(request))
    try:
        mbu = MeritBadgeUniversity.objects.get(current=True)
    except MeritBadgeUniversity.DoesNotExist:
        mbu = None
    if mbu is not None:
        sessions = TimeBlock.objects.filter(mbu=mbu).values('pk')
        course_instances = CourseInstance.objects.filter(session__pk__in=sessions)
        args.update({'classlist': course_instances })
    return render(request, 'mbu/classlist.html', args)


def view_class_requirements(request, id=-1):
    args = {}
    args.update(csrf(request))
    #if (id < 0):
        #handle error
    args.update({'id': id})
    return render(request, 'mbu/classrequirements.html', args)


def view_reports(request):
    return render(request, 'mbu/reports.html')


@permission_required('mbu.edit_scout_schedule', raise_exception=True)
def scout_edit_classes(request):
    args = {}
    user = request.user
    form = EditClassesForm(user=user)
    if request.POST:
        form = EditClassesForm(request.POST, user=user)
        if form.is_valid():
            user.enrollments.clear()
            for name, course_instance in form.cleaned_data.items():
                if course_instance is not None:
                    user.enrollments.add(course_instance)
            user.save()
            messages.add_message(request, messages.SUCCESS, 'Your schedule has been updated.')
            return redirect('mbu_home')

    args.update({'form': form})
    args.update(csrf(request))

    course_catalog = CourseInstance.objects.exclude(enrollees=user)
    args.update({'course_catalog': course_catalog})
    course_enrollments = user.enrollments.all()
    args.update({'course_enrollments': course_enrollments})
    return render(request, 'mbu/edit_classes.html', args)


@require_http_methods(["POST"])
def enroll_course(request):
    course_instance_id = request.POST.get('course_instance_id')
    course_instance = CourseInstance.objects.get(pk=course_instance_id)
    user = request.user
    user.enrollments.add(course_instance)
    user.save()
    return HttpResponse(request.GET.get('course_instance_id'))

@require_http_methods(["POST"])
def unenroll_course(request):
    course_instance_id = request.POST.get('course_instance_id')
    course_instance = CourseInstance.objects.get(pk=course_instance_id)
    user = request.user
    user.enrollments.remove(course_instance)
    user.save()
    return HttpResponse(request.GET.get('course_instance_id'))


def view_registered_classes(request):
    args = {}
    user = request.user
    enrolled_courses = user.enrollments.all()
    args.update({'enrolled_courses': enrolled_courses})
    return render(request, 'mbu/view_classes.html', args)


def view_troop_enrollees(request):
    args = {}
    scoutmaster = Scoutmaster.objects.get(user=request.user)
    troop = Troop.objects.get(scoutmaster=scoutmaster)
    scouts = Scout.objects.all().filter(troop=troop)
    args.update({'scouts': scouts})
    return render(request, 'scoutmaster/view_troop.html', args)


def sm_signup(request):
    pass


def sm_complete_signup(request, key=None):
    form = MbuUserCreationForm()
    if request.POST:
        form = MbuUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Scoutmaster(user=user).save()
            ct = ContentType.objects.get(app_label='mbu', model='scoutmaster')
            perms = [
                Permission.objects.get(codename='can_modify_troop_enrollments', content_type=ct),
                Permission.objects.get(codename='edit_scoutmaster_profile', content_type=ct)
            ]
            for perm in perms:
                user.user_permissions.add(perm)
            user.save()
            messages.add_message(request, messages.SUCCESS, 'Successfully registered.')
            return redirect('mbu_home')
    email = ScoutmasterRequest.objects.get(key=key).email
    form.fields['email'].initial = email
    form.fields['email'].widget.attrs['readonly'] = True
    args = {'form': form}
    args.update({'route': 'mbu.views.sm_complete_signup'})
    args.update({'key': key})
    return render(request, 'mbu/sm_signup.html', args)


def sm_view_class(request, scout_id):
    args = {}
    course_enrollments = Scout.objects.get(pk=scout_id).user.enrollments.all()
    args.update({'course_enrollments': course_enrollments})
    print (course_enrollments)
    return render(request, 'scoutmaster/view_troop_courses.html', args)


def populate_courses(request):
    _populate_courses()
    messages.add_message(request, messages.SUCCESS, 'Courses updated.')
    return redirect('mbu_home')

def pay_with_paypal(request):

    paypal_dict = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': '100', # calculate this amount dynamically
        'item_name': 'MBU 2015', #change this dynamically
        'invoice': 1, # generate invoice id from database
        'notify_url': 'http://localhost:8000' + reverse('paypal-ipn'),
        'return_url': 'http://localhost:8000', # set this to user's home page
        'cancel_return': 'http://localhost:8000' # set to user's home page
    }

    form = PayPalPaymentsForm(initial=paypal_dict)
    args = {'form': form}
    return render(request, 'mbu/payment.html', args)