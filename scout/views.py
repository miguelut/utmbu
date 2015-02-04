from django.shortcuts import render, render_to_response
from scout.forms import EditClassesForm

# Create your views here.
def edit_classes(request):
	form = EditClassesForm()
	args = {}
	args.update({'form': form})
	return render_to_response('scout/edit_classes.html', args)