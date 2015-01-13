from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views

#General Views
urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'mbu.views.home', name = 'mbu_home'),
    url(r'^profile/edit/', 'mbu.views.edit_profile', name = 'edit_profile'),
    url(r'^classlist/', 'mbu.views.classlist', name = 'class_list'),
    url(r'^classrequirements/(\d)/$', 'mbu.views.classrequirements', name = 'class_requirements')
)

#Authentication Views
urlpatterns += patterns(
    '',
    url(r'^login/$', 'django.contrib.auth.views.login', { 'template_name': 'login.html' },  name = 'login'),
    url(r'^logout/$', 'mbu.views.logout_user', name = 'logout'),
)

# Scout URLS
urlpatterns += patterns(
    '',
    url(r'^scout/register/', 'mbu.views.register_scout', name = 'register_scout'),
    url(r'^scoutmaster/', 'mbu.views.scoutmaster', name = 'scoutmaster'),
)