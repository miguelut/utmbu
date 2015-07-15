from mbu.models import Scout

def user_get_names(backend, details, response, is_new=False, *args, **kwargs):
    data = backend.strategy.request_data();
    user = details
    if (backend == 'facebook'):
        user.first_name = response.get('first_name')
        user.last_name = response.get('last_name')
    user.save()

def user_make_scout(backend, details, response, is_new=False, *args, **kwargs):
    user = kwargs.get('user')
    scout = Scout.objects.get(user=user)
    if(scout is None):
        Scout(user=user).save()