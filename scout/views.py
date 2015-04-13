from django.shortcuts import render, redirect
from django.core.context_processors import csrf
from django.contrib.auth.decorators import permission_required
from django.contrib import messages
from scout.forms import EditClassesForm
from course.models import CourseInstance

# Create your views here.
@permission_required('scout.edit_scout_schedule',raise_exception=True)
def edit_classes(request):
    args = {}
    user = request.user
    form = EditClassesForm(user=user)
    if request.POST:
        form = EditClassesForm(request.POST, user=user)
        if form.is_valid():
            user.enrollments.clear()
            for name, course_instance in form.cleaned_data.items():
                if course_instance is not None:
                    user.enrollments.add(course_instance)
            user.save()
            messages.add_message(request, messages.SUCCESS, 'Your schedule has been updated.')
            return redirect('mbu_home')

    args.update({'form': form})
    args.update(csrf(request))
    return render(request, 'scout/edit_classes.html', args)

def view_registered_classes(request):
    args = {}
    user = request.user
    enrolled_courses = user.enrollments.all()
    args.update({'enrolled_courses': enrolled_courses})
    return render(request, 'scout/view_classes.html', args)
