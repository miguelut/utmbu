import logging
from django.db.models import Count
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect, render_to_response
from django.core.context_processors import csrf
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import permission_required, user_passes_test
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import Permission, ContentType
from django.views.decorators.csrf import csrf_exempt
from paypal.standard.forms import PayPalPaymentsForm
from mbu.forms import *
from mbu.models import *
from mbu.util import _is_user_scout, _is_user_scoutmaster, _is_user_parent
from django.conf import settings
from decimal import Decimal
from mbu.api.course_instance import *
from mbu.api.scout import *
from mbu.api.parent import *
from mbu.api.scoutmaster import *
from mbu.api.troop import *

logger = logging.getLogger(__name__)


def signup(request):
    """This is the default signup method.
    This method will register a user and a corresponding Scout."""
    form = MbuUserCreationForm()
    if request.POST:
        form = MbuUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user = authenticate(username=user.username, password=form.data['password1'])
            auth_login(request, user)
            args = {'action': '/create?'}
            return render(request, 'mbu/select_type.html', args)
    args = {'form': form}
    return render(request, 'mbu/signup.html', args)


def create(request):
    type = request.GET['type']
    if type == 'scout':
        return create_scout(request)
    elif type == 'parent':
        return create_parent(request)
    elif type == 'scoutmaster':
        return create_scoutmaster(request)


def create_scout(request):
    user = request.user
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
    messages.add_message(request, messages.INFO, 'Please complete your profile below.')
    return redirect('scout_edit_profile')


def create_parent(request):
    user = request.user
    Parent(user=user).save()
    ct = ContentType.objects.get(app_label='mbu', model='parent')
    perms = [
        Permission.objects.get(codename='parent_edit_scout_schedule', content_type=ct),
        Permission.objects.get(codename='edit_parent_profile', content_type=ct)
    ]
    for perm in perms:
        user.user_permissions.add(perm)
    user.save()
    messages.add_message(request, messages.SUCCESS, 'Successfully registered.')
    messages.add_message(request, messages.INFO, 'Please complete your profile below.')
    return redirect('parent_edit_profile')


def create_scoutmaster(request):
    user = request.user
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
    messages.add_message(request, messages.INFO, 'Please complete your profile below.')
    return redirect('sm_edit_profile')


def login(request):
    args = {}
    form = AuthenticationForm()
    next_page = request.POST.get('next', request.GET.get('next', '/'))
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect(next_page)
        messages.add_message(request, messages.ERROR, 'Invalid username or password')
    args.update({'form': form})
    args.update({'next': next_page})
    return render(request, 'login.html', args)


def logout_user(request):
    logout(request)
    return redirect('mbu_home')


@csrf_exempt
def view_home_page(request):
    if _is_user_scout(request.user):
        return _render_scout_homepage(request)
    elif _is_user_parent(request.user):
        return _render_parent_homepage(request)
    elif _is_user_scoutmaster(request.user):
        return _render_scoutmaster_homepage(request)
    return render(request, 'mbu/home.html')


def _render_scout_homepage(request):
    scout = Scout.objects.get(user=request.user)
    if scout.troop is None or scout.rank == '':
        messages.add_message(request, messages.INFO, 'Please complete your profile below.')
        return redirect('scout_edit_profile')
    args = {'enrollments': scout.enrollments.all()}
    return render(request, 'mbu/scout_home.html', args)


def _render_parent_homepage(request):
    parent = Parent.objects.get(user=request.user)
    if parent.troop is None:
        messages.add_message(request, messages.INFO, 'Please complete your profile below.')
        return redirect('parent_edit_profile')
    args = {}
    troop = parent.troop
    scouts = parent.scouts.all()
    scouts_and_enrollments = _create_scout_enrollment_dict(scouts)
    args.update({'scouts_and_enrollments': scouts_and_enrollments})
    args.update({'troop': troop})
    return render(request, 'mbu/parent_home.html', args)


def _render_scoutmaster_homepage(request):
    scoutmaster = Scoutmaster.objects.get(user=request.user)
    if scoutmaster.troop is None:
        messages.add_message(request, messages.INFO, 'Please complete your profile below.')
        return redirect('sm_edit_profile')
    args = {}
    troop = Troop.objects.get(scoutmaster=scoutmaster)
    scouts = Scout.objects.all().filter(troop=troop)
    scouts_and_enrollments = _create_scout_enrollment_dict(scouts)
    args.update({'scouts_and_enrollments': scouts_and_enrollments})
    args.update({'troop': troop})

    return render(request, 'mbu/scoutmaster_home.html', args)


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


@user_passes_test(_is_user_parent, login_url='/login/')
def edit_parent_profile(request):
    args = {}
    parent_form = ParentProfileForm
    parent = Parent(user=request.user)
    try:
        parent = Parent.objects.get(user=request.user)
    except Parent.DoesNotExist:
        pass

    return _edit_profile(request, parent_form, parent, args)


def _edit_profile(request, ProfileForm, user, args):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=user)
        if form.is_valid() and profile_form.is_valid():
            form.save()
            profile_form.save()
            messages.add_message(request, messages.SUCCESS, 'Your profile has been saved.')
            return redirect('mbu_home')
    else:
        form = UserProfileForm(instance=request.user)
        profile_form = ProfileForm(instance=user)
    args.update({'form': form})
    args.update({'profile_form': profile_form})
    args.update({'troop_form': TroopModalForm()})
    return render(request, 'mbu/edit_profile.html', args)


def view_class_list(request):
    args = {}
    args.update(csrf(request))
    try:
        mbu = MeritBadgeUniversity.objects.get(current=True)
    except MeritBadgeUniversity.DoesNotExist:
        mbu = None
    if mbu is not None:
        timeblocks = TimeBlock.objects.filter(mbu=mbu).values('pk')
        course_instances = ScoutCourseInstance.objects.filter(timeblock__pk__in=timeblocks)
        args.update({'classlist': course_instances})
    return render(request, 'mbu/classlist.html', args)


def view_class_requirements(request, id=-1):
    args = {}
    args.update(csrf(request))
    args.update({'id': id})
    return render(request, 'mbu/classrequirements.html', args)


@permission_required('mbu.edit_scout_schedule', raise_exception=True)
@user_passes_test(_is_user_scout, login_url='/login/')
def scout_edit_classes(request):
    scout = Scout.objects.get(user=request.user)
    endpoint = '/api/scout/enrollments/'
    return _render_edit_classes(request, scout, endpoint)


def _render_edit_classes(request, scout, endpoint):
    args = {}
    args.update({'timeblocks': TimeBlock.objects.all()})
    args.update({'scout_id': scout.id})
    args.update({'endpoint': endpoint})
    args.update(csrf(request))

    return render(request, 'mbu/edit_classes.html', args)


def view_registered_classes(request):
    args = {}
    scout = Scout.objects.get(user=request.user)
    enrolled_courses = scout.enrollments.all()
    args.update({'enrolled_courses': enrolled_courses})
    return render(request, 'mbu/view_classes.html', args)


def _create_scout_enrollment_dict(scouts):
    scout_course_dict = {}
    for scout in scouts:
        course_enrollments = Scout.objects.get(pk=scout.pk).enrollments.all()
        scout_course_dict[scout] = course_enrollments
    return scout_course_dict


@permission_required('mbu.can_modify_troop_enrollments', raise_exception=True)
@user_passes_test(_is_user_scoutmaster, login_url='/login/')
def sm_edit_scout_classes(request, scout_id):
    scout = Scout.objects.get(pk=scout_id)
    endpoint = '/api/scoutmaster/enrollments/'
    return _render_edit_classes(request, scout, endpoint)


@user_passes_test(_is_user_scoutmaster, login_url='/login/')
def sm_view_troop_payments(request):
    args = {'data': []}
    scoutmaster = Scoutmaster.objects.get(user=request.user)
    troop = Troop.objects.get(scoutmaster=scoutmaster)
    scouts = Scout.objects.all().filter(troop=troop)
    for scout in scouts:
        payments = Payment.objects.all().filter(user=scout.user, status=settings.PAYMENT_PROCESSED)
        args['data'].append(_create_scout_payment_data(scout, payments))
    return render(request, 'mbu/sm_report_troop_payments.html', args)


@permission_required('mbu.can_modify_troop_enrollments', raise_exception=True)
@user_passes_test(_is_user_scoutmaster, login_url='/login/')
def sm_add_scouts(request):
    return render(request, 'mbu/sm_add_scouts.html')


@user_passes_test(_is_user_scout, login_url='/login/')
def scout_view_payments(request):
    scout = Scout.objects.get(user=request.user)
    args = _get_payment_report_data([scout])
    return render(request, 'mbu/scout_report_payments.html', args)


def _create_scout_payment_data(scout, payments):
    amount_invoiced = _get_amount_invoiced(scout)
    amount_paid = _get_amount_paid(payments)
    amount_owed = Decimal(amount_invoiced) - Decimal(amount_paid)
    return {
        'scout': scout,
        'amount_owed': amount_owed,
        'amount_invoiced': amount_invoiced,
        'amount_paid': amount_paid
    }


def _get_amount_invoiced(scout):
    enrollments = scout.enrollments.all()
    number_of_enrollments = 0
    for e in enrollments:
        number_of_enrollments += 1
        if e.timeblock.double:
            number_of_enrollments += 1
        if e.timeblock.all_day:
            number_of_enrollments += 3
    return Decimal(settings.PRICE_PER_COURSE * number_of_enrollments)


def _get_amount_paid(payments):
    amount = Decimal(0.00)
    for payment in payments:
        amount += Decimal(payment.amount)
    return amount


@permission_required('mbu.parent_edit_scout_schedule', raise_exception=True)
@user_passes_test(_is_user_parent, login_url='/login/')
def parent_add_scouts(request):
    return render(request, 'mbu/parent_add_scouts.html')


@permission_required('mbu.parent_edit_scout_schedule', raise_exception=True)
@user_passes_test(_is_user_parent, login_url='/login/')
def parent_edit_scout_classes(request, scout_id):
    scout = Scout.objects.get(pk=scout_id)
    endpoint = '/api/parent/enrollments/'
    return _render_edit_classes(request, scout, endpoint)


@permission_required('mbu.parent_edit_scout_schedule', raise_exception=True)
@user_passes_test(_is_user_parent, login_url='/login/')
def parent_payments(request):
    parent = Parent.objects.get(user=request.user)
    scouts = Scout.objects.filter(parent=parent)
    args = _get_payment_report_data(scouts)

    return render(request, 'mbu/scout_report_payments.html', args)


def _get_payment_report_data(scouts):
    args = {
        "amount_owed": Decimal(0.00),
        "amount_paid": Decimal(0.00),
        "amount_invoiced": Decimal(0.00),
        "payments": []
    }
    payments_for_set = []
    for scout in scouts:
        payments = Payment.objects.filter(user=scout.user, status=settings.PAYMENT_PROCESSED)
        data = _create_scout_payment_data(scout, payments)
        args["amount_owed"] += data["amount_owed"]
        args["amount_paid"] += data["amount_paid"]
        args["amount_invoiced"] += data["amount_invoiced"]
        args["payments"].extend(payments)

        if data["amount_owed"] != Decimal(0.00):
            try:
                payment = Payment.objects.get(user=scout.user, status=settings.PAYMENT_NEW)
                payment.amount = data["amount_owed"]
            except:
                payment = Payment.objects.create(user=scout.user, amount=data["amount_owed"], status=settings.PAYMENT_NEW)

            payment.save()
            payments_for_set.append(payment)

    payment_set = _get_new_payment_set(payments_for_set)
    paypal_dict = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': args["amount_owed"],
        'item_name': 'MBU 2016', # change this dynamically
        'notify_url': settings.PAYPAL_NOTIFY_URL + reverse('paypal-ipn'),
        'return_url': settings.PAYPAL_RETURN_URL,  # set this to user's home page
        'cancel_return': settings.PAYPAL_CANCEL_RETURN,  # set to user's home page
        'custom': payment_set.id
    }

    form = PayPalPaymentsForm(initial=paypal_dict)
    args.update({'form': form})
    return args


def show_faq(request):
    return render(request, 'mbu/faq.html')


def _get_new_payment_set(payments):
    payment_set = PaymentSet.objects.create()
    for payment in payments:
        assert(payment.status == settings.PAYMENT_NEW)
        PaymentSet.objects.filter(payments__id__contains=payment.id).delete()
        payment_set.payments.add(payment)
    payment_set.save()
    return payment_set
