from django.shortcuts import render, redirect
from troop.models import Troop, Council
from scout.models import Scout
from scoutmaster.models import Scoutmaster
from mbu.models import MeritBadgeUniversity
from datetime import datetime

# Create your views here.
def setup_dummy_data(request):
    council, create = Council.objects.get_or_create(name='Test Council')
    council.save()
    troop, create = Troop.objects.get_or_create(number='464', council=council)
    council.save()
    mbu, create = MeritBadgeUniversity.objects.get_or_create(name='MBU 2015', year=datetime.today(), current=True)
    return redirect('mbu_home')
