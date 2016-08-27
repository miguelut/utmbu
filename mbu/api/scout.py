from django.http import JsonResponse
from rest_framework.decorators import api_view
from mbu.models import Scout, ScoutCourseInstance, ScoutCourseInstanceSerializer

__author__ = 'michael'


@api_view(http_method_names=['GET', 'POST'])
def enrollments(request):
    user = request.user
    scout = Scout.objects.get(user=user)
    scout_enrollments = []
    if request.method == 'POST':
        for d in request.data:
            scout_enrollments.append(ScoutCourseInstance.objects.get(pk=d['id']))

        scout.enrollments = scout_enrollments
        scout.save()
        return JsonResponse({'data': request.data})
    else:
        for enrollment in ScoutCourseInstance.objects.filter(enrollees__user__pk__contains=scout.user.pk):
            serializer = ScoutCourseInstanceSerializer(enrollment)
            scout_enrollments.append(serializer.data)
        result = {'enrollments': scout_enrollments}
        return JsonResponse(result)
