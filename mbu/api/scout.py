from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse
from django.contrib.auth.decorators import permission_required
from rest_framework.decorators import api_view
from mbu.models import Scout, ScoutCourseInstance, ScoutCourseInstanceSerializer, RegistrationStatus

__author__ = 'michael'


@permission_required('mbu.edit_scout_schedule', raise_exception=True)
@api_view(http_method_names=['GET', 'POST'])
def scout_enrollments(request, scout_id):
    user = request.user
    scout = Scout.objects.get(user=user)
    scout_check = Scout.objects.get(pk=scout_id)
    assert(scout == scout_check)
    enrollments = []
    if request.method == 'POST' and _reg_is_open():
        for d in request.data:
            enrollments.append(ScoutCourseInstance.objects.get(pk=d['id']))

        scout.enrollments = enrollments
        scout.save()
        return JsonResponse({'data': request.data})
    else:
        for enrollment in scout.enrollments.all():
            serializer = ScoutCourseInstanceSerializer(enrollment)
            enrollments.append(serializer.data)
        result = {'enrollments': enrollments}
        return JsonResponse(result)


@staff_member_required
@api_view(http_method_names=['POST'])
def check_in_scouts(request, scout_id):
    scout = Scout.objects.get(pk=scout_id)
    scout.checked_in = True
    scout.save()
    result = {"scout": scout_id}
    return JsonResponse(result)


def _reg_is_open():
    status = RegistrationStatus.objects.first()
    if status:
        status = status.status

    return status == 'OPEN'
