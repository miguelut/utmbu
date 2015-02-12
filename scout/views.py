from django.shortcuts import render, render_to_response
from django.core.context_processors import csrf
from django.contrib.auth.decorators import permission_required
from scout.forms import EditClassesForm
from course.models import CourseInstance

# Create your views here.
@permission_required('scout.edit_scout_schedule',raise_exception=True)
def edit_classes(request):
    args = {}
    if request.POST:
        user = request.user
        form = EditClassesForm(request.POST)
        if form.is_valid():
            for name, course_instance in form.cleaned_data.items():
                if course_instance is not None:
                    user.course_instances.add(course_instance)
            user.save()

    args.update({'form': EditClassesForm()})
    args.update(csrf(request))
    return render(request, 'scout/edit_classes.html', args)
