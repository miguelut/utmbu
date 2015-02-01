from django.shortcuts import render, render_to_response
from django.core.context_processors import csrf
from django.forms import ModelForm
from course.models import Course, Session

# Create your views here.
class CourseForm(ModelForm):
    class Meta:
        model = Course
        fields = ['name']

class SessionForm(ModelForm):
    class Meta:
        model = Session
        exclude = []

def add_course(request):
    args = {}
    args.update(csrf(request))
    args.update({'form':CourseForm()})
    if request.POST:
        c = Course()
        c.name = request.POST.get('name')
        c.save()
        return render_to_response('mbu/home.html')
    return render_to_response('course/add_course.html', args)
