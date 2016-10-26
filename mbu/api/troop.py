from django.http import JsonResponse
from django.contrib.auth.decorators import permission_required
from rest_framework.decorators import api_view
from mbu.models import Scout, ScoutCourseInstance, ScoutCourseInstanceSerializer, Scoutmaster, Troop, Council, \
    TroopSerializer

__author__ = 'michael'


@api_view(http_method_names=['POST'])
def add_troop(request):
    if request.method == 'POST':
        number = request.data['troop_number']
        council = Council.objects.get(pk=request.data['council_id'])
        troop, created = Troop.objects.get_or_create(number=number, council=council)
        serializer = TroopSerializer(troop)
        return JsonResponse(serializer.data)
