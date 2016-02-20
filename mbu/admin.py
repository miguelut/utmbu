from django.contrib import admin
from mbu.models import *

# Register your models here.

admin.site.register(MeritBadgeUniversity)
admin.site.register(Council)
admin.site.register(Troop)
admin.site.register(Scout)
admin.site.register(Scoutmaster)
admin.site.register(Course)
admin.site.register(TimeBlock)
admin.site.register(ScoutCourseInstance)
admin.site.register(ScoutmasterRequest, ScoutmasterRequestAdmin)
admin.site.register(Payment)