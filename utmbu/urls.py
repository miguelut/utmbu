from django.conf.urls import patterns, include, url
from django.contrib import admin

#General Views
urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
    url('', include('social.apps.django_app.urls', namespace='social')),
    url(r'^$', 'mbu.views.view_home_page', name='mbu_home'),
    url(r'^class/list/$', 'mbu.views.view_class_list', name='class_list'),
    url(r'^class/requirements/(\d)/$', 'mbu.views.view_class_requirements', name='class_requirements'),
    url(r'^register/scout/$', 'mbu.views.register_user_as_scout', name='register_scout'),
    url(r'^register/scoutmaster/$', 'mbu.views.register_user_as_scoutmaster', name='register_scoutmaster'),
    url(r'^populate_courses/$', 'mbu.views.populate_courses', name='populate_courses'),
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
    url(r'^scoutmaster/register/$', 'mbu.views.sm_signup', name='sm_signup'),
    url(r'^scoutmaster/register/complete/(?P<key>.+)$', 'mbu.views.sm_complete_signup', name='sm_complete_signup'),
    url(r'^scoutmaster/troop/$', 'mbu.views.view_troop_enrollees', name='sm_view_troop'),
    url(r'^scoutmaster/viewclasses/(?P<scout_id>\d)/$', 'mbu.views.sm_view_class', name='sm_view_classes'),
    url(r'^scoutmaster/profile/edit/$', 'mbu.views.edit_scoutmaster_profile', name='sm_edit_profile'),
    url(r'^scoutmaster/troop/report/payments/$', 'mbu.views.sm_view_troop_payments', name='sm_report_troop_payments')
)

#Paypal URLS
urlpatterns += patterns(
    '',
    url(r'^pay', 'mbu.views.pay_with_paypal', name='pay-with-paypal'),
    url(r'^paypal/notify', include('paypal.standard.ipn.urls'))
)

#Dev URLs -- REMOVE BEFORE DEPLOYMENT
urlpatterns += patterns(
    '',
    url(r'^setup_data/', 'dev.views.setup_data', name='setup_data')
)

#Rest Calls
urlpatterns += patterns(
    '',
    url(r'^api/courses', 'mbu.views.courses', name='api_courses'),
    url(r'^api/enrollments', 'mbu.views.enrollments', name='api_enrollments')
)
