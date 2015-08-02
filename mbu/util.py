import json
import urllib
import hashlib
from django.core.mail import send_mail
from mbu.models import Scout, Scoutmaster, Course

__author__ = 'michael'

def _is_user_scout(user):
    if Scout.objects.filter(user=user.id).count() > 0:
        return True
    return False


def _is_user_scoutmaster(user):
    if Scoutmaster.objects.filter(user=user.id).count() > 0:
        return True
    return False


def _populate_courses():
    """This method relies on a data format provided by http://www.meritbadge.org
    If the format of the returned data or the URL of the site changes this method
    will need to be updated accordingly."""
    url = 'http://www.meritbadge.org/wiki/api.php?action=query&list=categorymembers&cmtitle=Category:Merit_badges&cmlimit=500&cmnamespace=0&format=json'
    req = urllib.request.Request(url, headers = {'User-Agent': 'Magic Browser'})
    with urllib.request.urlopen(req) as request:
        json_str = request.read().decode('utf-8')
        result = json.loads(json_str)
        members = result['query']['categorymembers']
        for member in members:
            Course.objects.get_or_create(name=member['title'])


def _get_hash_str():
    return hashlib.sha256().hexdigest()


def _send_sm_request_email(email=None, key=None):
    send_mail('MBU Test Subject', 'This is a test. %s' % key, 'UTMBU Registration <mbu@vexule.com>', [email])
