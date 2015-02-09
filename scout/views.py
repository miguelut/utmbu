from django.shortcuts import render, render_to_response
from django.forms.formsets import formset_factory
from scout.forms import EditClassesForm
from mbu.models import MeritBadgeUniversity
from course.models import Session

# Create your views here.
def edit_classes(request):
    args = {}
    args.update({'form': EditClassesForm()})
    return render_to_response('scout/edit_classes.html', args)


