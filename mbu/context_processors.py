from django.conf import settings
from mbu.util import _is_user_scoutmaster, _is_user_scout

def default_links(request):
    """Adds the variable DEFAULT_LINKS to the request context."""
    return { 'DEFAULT_LINKS' : settings.DEFAULT_LINKS }

def add_links(request):
    user = request.user
    if user.is_authenticated():
        return _get_links(user)
    else:
        return {}

def _get_links(user):
    args = { 'links': []}
    if(_is_user_scout(user)):
        args.get('links').append({
            'href': 'scout_edit_classes',
            'label':'Add/Edit Classes'
        })
        args.get('links').append({
            'href': 'scout_edit_profile',
            'label': 'Edit Profile'
        })
    elif(_is_user_scoutmaster(user)):
        args.get('links').append({
            'href': 'sm_view_troop',
            'label': 'View Scout Classes'
        })
        args.get('links').append({
            'href': 'sm_edit_profile',
            'label': 'Edit Profile'
        })
    return args
