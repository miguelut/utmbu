__author__ = 'michael'
from mbu.models import Scout, Scoutmaster

def _is_user_scout(user):
    if Scout.objects.filter(pk=user.id).count() == 1:
        return True
    return False


def _is_user_scoutmaster(user):
    if Scoutmaster.objects.filter(pk=user.id).count() == 1:
        return True
    return False

