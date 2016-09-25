from django.http import JsonResponse
from django.contrib.auth.decorators import permission_required
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from mbu.models import Parent, Scout


@permission_required('mbu.parent_edit_scout_schedule', raise_exception=True)
@api_view(http_method_names=['POST'])
def registerscouts(request):
    parent = Parent.objects.get(user=request.user)
    for scout_data in request.data:
        user = User.objects.create_user(
            scout_data['username'],
            email=scout_data['email'],
            password=scout_data['password'],
            first_name=scout_data['fname'],
            last_name=scout_data['lname']
        )
        scout = Scout.objects.create(
            user=user,
            troop=parent.troop,
            rank=scout_data['rank'],
            parent=parent
        )

    return JsonResponse({'response': 'Success'})
