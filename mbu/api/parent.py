from django.contrib.contenttypes.models import ContentType
from django.http import JsonResponse
from django.contrib.auth.decorators import permission_required
from rest_framework.decorators import api_view
from django.contrib.auth.models import User, Permission
from mbu.models import Parent, Scout, ScoutCourseInstance, ScoutCourseInstanceSerializer, RegistrationStatus


@permission_required('mbu.parent_edit_scout_schedule', raise_exception=True)
@api_view(http_method_names=['POST'])
def parent_registerscouts(request):
    if _reg_is_open():
        parent = Parent.objects.get(user=request.user)
        for scout_data in request.data:
            user = User.objects.create_user(
                scout_data['username'],
                email=scout_data['email'],
                password=scout_data['password'],
                first_name=scout_data['fname'],
                last_name=scout_data['lname']
            )
            ct = ContentType.objects.get(app_label='mbu', model='scout')
            perms = [
                Permission.objects.get(codename='edit_scout_schedule', content_type=ct),
                Permission.objects.get(codename='edit_scout_profile', content_type=ct)
            ]
            for perm in perms:
                user.user_permissions.add(perm)
            user.save()
            scout = Scout.objects.create(
                user=user,
                troop=parent.troop,
                rank=scout_data['rank'],
                parent=parent
            )

    return JsonResponse({'response': 'Success'})


@permission_required('mbu.parent_edit_scout_schedule', raise_exception=True)
@api_view(http_method_names=['POST', 'GET'])
def parent_enrollments(request, scout_id):
    user = request.user
    parent = Parent.objects.get(user=user)
    scout = Scout.objects.get(pk=scout_id)
    assert(parent == scout.parent)
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


@permission_required('mbu.parent_edit_scout_schedule', raise_exception=True)
@api_view(http_method_names=['POST'])
def api_parent_waiver(request, scout_id):
    user = request.user
    parent = Parent.objects.get(user=user)
    scout = Scout.objects.get(pk=scout_id)
    assert(scout.parent == parent)
    scout.waiver = True
    scout.save()
    return JsonResponse({'result': 'success'})


def _reg_is_open():
    status = RegistrationStatus.objects.first()
    if status:
        status = status.status

    return status == 'OPEN'