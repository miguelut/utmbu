from django.http import JsonResponse
from django.contrib.auth.decorators import permission_required
from rest_framework.decorators import api_view
from mbu.models import Scout, ScoutCourseInstance, ScoutCourseInstanceSerializer

__author__ = 'michael'


@permission_required('mbu.edit_scout_schedule', raise_exception=True)
@api_view(http_method_names=['GET', 'POST'])
def scout_enrollments(request, scout_id):
    user = request.user
    scout = Scout.objects.get(user=user)
    scout_check = Scout.objects.get(pk=scout_id)
    assert(scout == scout_check)
    enrollments = []
    if request.method == 'POST':
        for d in request.data:
            enrollments.append(ScoutCourseInstance.objects.get(pk=d['id']))

        scout.enrollments = enrollments
        scout.save()
        return JsonResponse({'data': request.data})
    else:
        for enrollment in ScoutCourseInstance.objects.filter(enrollees__user__pk__contains=scout.user.pk):
            serializer = ScoutCourseInstanceSerializer(enrollment)
            enrollments.append(serializer.data)
        result = {'enrollments': enrollments}
        return JsonResponse(result)
