from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType
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
        for enrollment in scout.enrollments.all():
            serializer = ScoutCourseInstanceSerializer(enrollment)
            enrollments.append(serializer.data)
        result = {'enrollments': enrollments}
        return JsonResponse(result)


@permission_required('mbu.can_modify_troop_enrollments', raise_exception=True)
@api_view(http_method_names=['POST'])
def scoutmaster_registerscouts(request):
    scoutmaster = Scoutmaster.objects.get(user=request.user)
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
            troop=scoutmaster.troop,
            rank=scout_data['rank'],
            parent=None
        )

    return JsonResponse({'response': 'Success'})
