from django.conf import settings

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
    return { 'links' : [
        {'href': 'mbu_home', 'label':'Surrogate Home'}
        ]}
