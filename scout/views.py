from django.shortcuts import render, render_to_response
from django.contrib.auth.decorators import permission_required
from scout.forms import EditClassesForm

# Create your views here.
@permission_required('scout.edit_scout_schedule',raise_exception=True)
def edit_classes(request):
    args = {}
    args.update({'form': EditClassesForm()})
    return render(request, 'scout/edit_classes.html', args)
