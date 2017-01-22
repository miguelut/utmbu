from mbu.models import RegistrationStatus
from django.shortcuts import redirect
from django.contrib import messages


def check_open(strategy, details, user=None, *args, **kwargs):
    status = RegistrationStatus.objects.first()
    if status:
        status = status.status

    if user is None and status != 'OPEN':
        messages.add_message(strategy.request, messages.ERROR, "No user associated with this social account found and registration is closed.")
        return redirect('mbu_home')
