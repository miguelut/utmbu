from django.http import JsonResponse
from rest_framework.decorators import api_view
from mbu.models import ScoutCourseInstance, ScoutCourseInstanceSerializer

__author__ = 'michael'


@api_view(http_method_names=['GET'])
def courses(request):
    all_courses = []
    for course in ScoutCourseInstance.objects.all():
        serializer = ScoutCourseInstanceSerializer(course)
        all_courses.append(serializer.data)
    result = {'courses': all_courses}
    return JsonResponse(result)
