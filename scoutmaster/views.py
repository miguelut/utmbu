from django.shortcuts import render, redirect
from troop.models import Troop
from scoutmaster.models import Scoutmaster
from scout.models import Scout
from course.models import CourseInstance
from django.contrib.auth.models import User
from scout.forms import EditClassesForm
from django.core.context_processors import csrf

# Create your views here.

def view_troop_enrollees(request):
    args = {}
    scoutmaster = Scoutmaster.objects.get(user=request.user)
    troop = Troop.objects.get(scoutmaster=scoutmaster)
    scouts = Scout.objects.all().filter(troop=troop)
    args.update({'scouts': scouts})
    return render(request, 'scoutmaster/view_troop.html', args)

def edit_troop_classes(request, scout_id):
    args = {}
    scout = Scout.objects.get(pk=scout_id)
    user = scout.user
    form = EditClassesForm(user=user)

    if request.POST:
        form = EditClassesForm(request.POST, user=user)
        if form.is_valid():
            user.enrollments.clear()
            for name, course_instance in form.cleaned_data.items():
                if course_instance is not None:
                    user.enrollments.add(course_instance)
            user.save()
            return redirect('scoutmaster_view_troop')

    args.update({'form': form})
    args.update(csrf(request))
    args.update({'scout': scout})

    return render(request, 'scoutmaster/view_troop_courses.html', args)