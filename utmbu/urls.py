from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views

#General Views
urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'mbu.views.view_home_page', name = 'mbu_home'),
    url(r'^profile/edit/', 'mbu.views.edit_profile', name = 'edit_profile'),
    url(r'^class/list/$', 'mbu.views.view_class_list', name = 'class_list'),
    url(r'^class/requirements/(\d)/$', 'mbu.views.view_class_requirements', name = 'class_requirements'),
    url(r'^class/schedule/$', 'mbu.views.view_class_schedule', name = 'class_schedule'),
    url(r'^reports/$', 'mbu.views.view_reports', name = 'reports'),
)

#Authentication Views
urlpatterns += patterns(
    '',
    url(r'^login/$', 'django.contrib.auth.views.login', { 'template_name': 'login.html' },  name = 'login'),
    url(r'^logout/$', 'mbu.views.logout_user', name = 'logout'),
)

# Registration URLS
urlpatterns += patterns(
    '',
    url(r'^scout/register/', 'registration.views.register_scout', name = 'register_scout'),
    url(r'^scoutmaster/register/', 'registration.views.register_scoutmaster', name = 'register_scoutmaster'),
)

#Course URLs
urlpatterns += patterns(
    '',
    url(r'^course/add', 'course.views.add_course', name = 'add_course')
)

# Scout URLS
urlpatterns += patterns(
    '',
    url(r'^scout/register/', 'mbu.views.register_scout', name = 'register_scout'),
    url(r'^scoutmaster/', 'mbu.views.view_scoutmaster_page', name = 'scoutmaster'),
)

#Course URLs
urlpatterns += patterns(
    '',
    url(r'^course/add', 'course.views.add_course', name = 'add_course')
)
