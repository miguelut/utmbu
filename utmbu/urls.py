from django.conf.urls import patterns, include, url
from django.contrib import admin
import mbu.paypal_signal_processor

#General Views
urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
    url('', include('social.apps.django_app.urls', namespace='social')),
    url(r'^$', 'mbu.views.view_home_page', name='mbu_home'),
    url(r'^create/$', 'mbu.views.create', name='create'),
    url(r'^class/list/$', 'mbu.views.view_class_list', name='class_list'),
    url(r'^class/requirements/(\d)/$', 'mbu.views.view_class_requirements', name='class_requirements'),
)

#Authentication Views
urlpatterns += patterns(
    '',
    url(r'^signup/$', 'mbu.views.signup', name='signup'),
    url(r'^login/$', 'mbu.views.login', name='login'),
    url(r'^logout/$', 'mbu.views.logout_user', name='logout'),
)

#Scout URLs
urlpatterns += patterns(
    '',
    url(r'^scout/editclasses/$', 'mbu.views.scout_edit_classes', name='scout_edit_classes'),
    url(r'^scout/viewclasses/$', 'mbu.views.view_registered_classes', name='scout_view_classes'),
    url(r'^scout/profile/edit/$', 'mbu.views.edit_scout_profile', name='scout_edit_profile'),
    url(r'^scout/report/payments/$', 'mbu.views.scout_view_payments', name='scout_report_payments'),
)

#Scoutmaster URLs
urlpatterns += patterns(
    '',
    url(r'^scoutmaster/editclasses/(?P<scout_id>\d+)/$', 'mbu.views.sm_edit_scout_classes', name='sm_edit_scout_classes'),
    url(r'^scoutmaster/profile/edit/$', 'mbu.views.edit_scoutmaster_profile', name='sm_edit_profile'),
    url(r'^scoutmaster/addscouts/$', 'mbu.views.sm_add_scouts', name='sm_add_scouts'),
    url(r'^scoutmaster/troop/report/payments/$', 'mbu.views.sm_view_troop_payments', name='sm_report_troop_payments')
)

#Parent Urls
urlpatterns += patterns(
    '',
    url(r'^parent/profile/edit/$', 'mbu.views.edit_parent_profile', name='parent_edit_profile'),
    url(r'^parent/addscouts/$', 'mbu.views.parent_add_scouts', name='parent_add_scouts'),
    url(r'^parent/editclasses/(?P<scout_id>\d+)/$', 'mbu.views.parent_edit_scout_classes', name='parent_edit_scout_classes'),
)

#Paypal URLS
urlpatterns += patterns(
    '',
    url(r'^paypal/', include('paypal.standard.ipn.urls'))
)

#Dev URLs -- REMOVE BEFORE DEPLOYMENT
urlpatterns += patterns(
    '',
    url(r'^setup_data/', 'dev.views.setup_data', name='setup_data')
)

#Rest Calls
urlpatterns += patterns(
    '',
    url(r'^api/courses/$', 'mbu.views.courses', name='api_courses'),
    url(r'^api/scout/enrollments/(?P<scout_id>\d+)$', 'mbu.views.scout_enrollments', name='api_scout_enrollments'),
    url(r'^api/scoutmaster/enrollments/(?P<scout_id>\d+)$', 'mbu.views.scoutmaster_enrollments', name='api_scoutmaster_enrollments'),
    url(r'^api/parent/enrollments/(?P<scout_id>\d+)$', 'mbu.views.parent_enrollments', name='api_parent_enrollments'),
    url(r'^api/parent/registerscouts', 'mbu.views.parent_registerscouts', name='api_parents_registerscourts'),
    url(r'^api/scoutmaster/registerscouts', 'mbu.views.scoutmaster_registerscouts', name='api_scoutmaster_registerscourts'),
    url(r'^api/troops', 'mbu.views.add_troop', name='api_add_troop')
)
