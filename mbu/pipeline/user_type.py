from mbu.models import Scout
from django.contrib.auth.models import Permission, ContentType

def user_get_names(backend, details, response, is_new=False, *args, **kwargs):
    user = details
    if (backend == 'facebook'):
        user.first_name = response.get('first_name')
        user.last_name = response.get('last_name')
    user.save()

def user_make_scout(backend, details, response, is_new=False, *args, **kwargs):
    user = kwargs.get('user')
    try:
        scout = Scout.objects.get(user=user.id)
    except:
        scout = None
    if(scout is None):
        Scout(user=user).save()
        ct = ContentType.objects.get(app_label='mbu', model='scout')
        perm = Permission.objects.get(codename='edit_scout_schedule', content_type=ct)
        user.user_permissions.add(perm)
        user.save()