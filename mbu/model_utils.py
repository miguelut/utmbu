import hashlib
from django.core.mail import send_mail

__author__ = 'michael'

def _get_hash_str():
    return hashlib.sha256().hexdigest()


def _send_sm_request_email(email=None, key=None):
    send_mail('MBU Test Subject', 'This is a test. %s' % key, 'UTMBU Registration <mbu@vexule.com>', [email])
