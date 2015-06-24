from social.pipeline.partial import partial
from django.shortcuts import render_to_response

@partial
def pick_profile(backend, details, response, is_new=False, *args, **kwargs):
    data = backend.strategy.request_data();
    if data.get('profile_type') is None:
        args = { 'backend_name' : backend.name }
        return render_to_response('mbu/choose_profile_pipeline.html', args)
    else:
        return
