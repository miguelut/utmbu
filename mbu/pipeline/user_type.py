from mbu.models import Scout
from django.contrib.auth.models import Permission, ContentType
from django.shortcuts import render_to_response
from social.pipeline.partial import partial


@partial
def get_type(backend, details, response, is_new=False, *args, **kwargs):
    if is_new:
        data = backend.strategy.request_data()
        if data.get('type') is None:
            args = {'action': '/complete/%s?' % backend.name}
            return render_to_response('mbu/select_type.html', args)
        else:
            return {'type': data.get('type')}


def user_create(backend, details, response, is_new=False, *args, **kwargs):
    if is_new:
        type = backend.strategy.request_data().get('type')
        if type == 'scout':
            user = kwargs.get('user')
            Scout(user=user).save()
            ct = ContentType.objects.get(app_label='mbu', model='scout')
            perm = Permission.objects.get(codename='edit_scout_schedule', content_type=ct)
            user.user_permissions.add(perm)
            user.save()
