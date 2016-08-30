from django.http import JsonResponse
from django.contrib.auth.decorators import permission_required
from rest_framework.decorators import api_view
from mbu.models import Scout, ScoutCourseInstance, ScoutCourseInstanceSerializer, Scoutmaster

__author__ = 'michael'


@permission_required('mbu.can_modify_troop_enrollments', raise_exception=True)
@api_view(http_method_names=['GET', 'POST'])
def scoutmaster_enrollments(request, scout_id):
    user = request.user
    scoutmaster = Scoutmaster.objects.get(user=user)
    troop = scoutmaster.troop
    scout = Scout.objects.get(pk=scout_id)
    assert(troop == scout.troop)
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
