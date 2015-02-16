from django.conf import settings

def default_links(request):
    """Adds the variable DEFAULT_LINKS to the request context."""
    return { 'DEFAULT_LINKS' : settings.DEFAULT_LINKS }