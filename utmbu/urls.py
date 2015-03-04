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
    url(r'^register/scout/', 'registration.views.register_scout', name = 'register_scout'),
    url(r'^register/scoutmaster/', 'registration.views.register_scoutmaster', name = 'register_scoutmaster'),
    url(r'^register/parent/', 'registration.views.register_parent', name = 'register_parent')
)

#Scout URLs
urlpatterns += patterns(
    '',
    url(r'^scout/editclasses/', 'scout.views.edit_classes', name = 'scout_edit_classes'),
    url(r'^scout/viewclasses/', 'scout.views.view_registered_classes', name = 'scout_view_classes')
)

#Dev URLs -- REMOVE BEFORE DEPLOYMENT
urlpatterns += patterns(
    '',
    url(r'^setup_dummy_data/', 'dev.views.setup_dummy_data', name ='setup_dummy_data')
)
