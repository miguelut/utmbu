from django.shortcuts import render
from troop.models import Troop
from scoutmaster.models import Scoutmaster
from scout.models import Scout

# Create your views here.

def view_troop_enrollees(request):
	args = {}
	scoutmaster = Scoutmaster.objects.get(user=request.user)
	troop = Troop.objects.get(scoutmaster=scoutmaster)
	scouts = Scout.objects.all().filter(troop=troop)
	args.update({'scouts': scouts})
	return render(request, 'scoutmaster/view_troop_classes.html', args)

def view_troop_classes(request, scout_id):
	args = {}
	return render(request, 'scoutmaster/view_troop_classes.html', args)