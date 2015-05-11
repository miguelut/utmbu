from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views

#General Views
urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url('', include('social.apps.django_app.urls', namespace='social')),
    url(r'^$', 'mbu.views.view_home_page', name='mbu_home'),
    url(r'^class/list/$', 'mbu.views.view_class_list', name='class_list'),
    url(r'^class/requirements/(\d)/$', 'mbu.views.view_class_requirements', name='class_requirements'),
    url(r'^reports/$', 'mbu.views.view_reports', name='reports'),
)

#Authentication Views
urlpatterns += patterns(
    '',
    url(r'^signup/$', 'mbu.views.signup', name='signup'),
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html'},  name='login'),
    url(r'^logout/$', 'mbu.views.logout_user', name='logout'),
)

#Scout URLs
urlpatterns += patterns(
    '',
    url(r'^scout/editclasses/$', 'mbu.views.edit_classes', name='scout_edit_classes'),
    url(r'^scout/viewclasses/$', 'mbu.views.view_registered_classes', name='scout_view_classes'),
    url(r'^scout/profile/edit/$', 'mbu.views.edit_scout_profile', name='edit_profile')
)

urlpatterns += patterns(
    '',
    url(r'^scoutmaster/viewtroop/$', 'mbu.views.view_troop_enrollees', name='scoutmaster_view_troop'),
    url(r'^scoutmaster/viewclasses/(?P<scout_id>\d)/$', 'mbu.views.view_troop_classes', name='scoutmaster_view_classes')
)

#Dev URLs -- REMOVE BEFORE DEPLOYMENT
urlpatterns += patterns(
    '',
    url(r'^setup_dummy_data/', 'dev.views.setup_dummy_data', name='setup_dummy_data')
)
