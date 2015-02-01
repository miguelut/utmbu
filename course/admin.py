from django.contrib import admin
from course.models import Course, Session

# Register your models here.
admin.site.register(Course)
admin.site.register(Session)

class SessionAdmin(admin.ModelAdmin):
    # If we want to add additional funcationality to the admin site
    # this is where we do it (?)
    pass
