from django.conf import settings
from mbu.models import RegistrationStatus
from mbu.util import _is_user_scoutmaster, _is_user_scout, _is_user_parent


def default_links(request):
    """Adds the variable DEFAULT_LINKS to the request context."""
    return {'DEFAULT_LINKS': settings.DEFAULT_LINKS}


def add_links(request):
    user = request.user
    if user.is_authenticated():
        return _get_links(user)
    else:
        return {}


def add_report_links(request):
    user = request.user
    if user.is_authenticated():
        return _get_report_links(user)
    else:
        return {}


def add_registration_status(request):
    status = RegistrationStatus.objects.first()
    if status:
        status = status.status

    return {'registration_status': status}


def _get_links(user):
    args = {'links': []}
    if _is_user_scout(user):
        args.get('links').append({
            'href': 'scout_edit_classes',
            'label': 'Add/Edit Classes'
        })
        args.get('links').append({
            'href': 'scout_edit_profile',
            'label': 'Edit Profile'
        })
    elif _is_user_scoutmaster(user):
        args.get('links').append({
            'href': 'sm_edit_profile',
            'label': 'Edit Profile'
        })
        args.get('links').append({
            'href': 'sm_add_scouts',
            'label': 'Register Scouts'
        })
    elif _is_user_parent(user):
        args.get('links').append({
            'href': 'parent_add_scouts',
            'label': 'Register Scouts'
        })
        args.get('links').append({
            'href': 'parent_edit_profile',
            'label': 'Edit Profile'
        })
    elif user.is_staff:
        args.get('links').append({
            'href': 'checkin',
            'label': 'Checkin'
        })
    args.get('links').append({
        'href': 'logout',
        'label': 'Logout'
    })


    return args


def _get_report_links(user):
    args = {'report_links': []}
    if _is_user_scout(user):
        args.get('report_links').append({
            'href': 'scout_report_payments',
            'label': 'Payments'
        })
    elif _is_user_scoutmaster(user):
        args.get('report_links').append({
            'href': 'sm_report_troop_payments',
            'label': 'Troop Payments'
        })
    elif _is_user_parent(user):
        args.get('report_links').append({
            'href': 'parent_report_payments',
            'label': 'Payments'
        })
        args.get('report_links').append({
            'href': 'parent_view_waivers',
            'label': 'Waivers'
        })
    elif user.is_staff:
        args.get('report_links').append({
            'href': 'roster_by_troop',
            'label': 'Troop Roster Report'
        })
        args.get('report_links').append({
            'href': 'roster_by_course',
            'label': 'Course Roster Report'
        })
    return args