from mbu.models import Scout, Scoutmaster, Course, Parent

__author__ = 'michael'

def _is_user_scout(user):
    if Scout.objects.filter(user=user.id).count() > 0:
        return True
    return False


def _is_user_scoutmaster(user):
    if Scoutmaster.objects.filter(user=user.id).count() > 0:
        return True
    return False


def _is_user_parent(user):
    if Parent.objects.filter(user=user.id).count() > 0:
        return True
    return False
