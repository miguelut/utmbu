from django.shortcuts import render
from troop.models import Troop
from scoutmaster.models import Scoutmaster
from scout.models import Scout
from course.models import CourseInstance
from django.contrib.auth.models import User

# Create your views here.

def view_troop_enrollees(request):
	args = {}
	scoutmaster = Scoutmaster.objects.get(user=request.user)
	troop = Troop.objects.get(scoutmaster=scoutmaster)
	scouts = Scout.objects.all().filter(troop=troop)
	args.update({'scouts': scouts})
	return render(request, 'scoutmaster/view_troop.html', args)

def view_troop_classes(request, scout_id):
	args = {}
	course_enrollments = Scout.objects.get(pk=scout_id).user.enrollments.all()
	args.update({'course_enrollments': course_enrollments})
	print (course_enrollments)
	return render(request, 'scoutmaster/view_troop_courses.html', args)