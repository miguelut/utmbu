import hashlib
from django.core.mail import EmailMultiAlternatives
from django.template import Context
from django.template.loader import get_template
from django.conf import settings

__author__ = 'michael'

def _get_hash_str(email=None):
    key = hashlib.sha256()
    key.update(email.encode())
    key.update(b'Elmertzilch')
    return key.hexdigest()


def _send_sm_request_email(email=None, key=None, troop=None):
    """This method will send the confirmation email to a Scoutmaster.

    Keyword arguments:
    email -- The email address of the Scoutmaster
    key -- a unique Sha256 key assigned to this request
    troop -- The troop the Scoutmaster belongs to
    """
    plaintext = get_template('mbu/sm_registration_email.txt')
    htmly = get_template('mbu/sm_registration_email.html')

    context = Context({
        'link': settings.SITE_URL + '/scoutmaster/register/complete/' + key,
        'email': email,
        'location': settings.MBU_LOCATION,
        'troop': troop.number,
        'countil': troop.council.name

    })

    subject, from_email = 'MBU Scoutmaster Registration', 'UTMBU Registration <mbu@vexule.com>'
    text_content = plaintext.render(context)
    html_content = htmly.render(context)
    msg = EmailMultiAlternatives(subject, text_content, from_email, [email])
    msg.attach_alternative(html_content, 'text/html')
    msg.send()