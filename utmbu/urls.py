from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views

#General Views
urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'utmbu.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    # url(r'^$', auth_views.login, {'template_name':'mbu/login.html'})
    url(r'^$', 'mbu.views.home', name = 'mbu_home')
)

#Authentication Views
urlpatterns += patterns(
	'django.contrib.auth.views',

	url(r'^login/', 'login',
		{'template_name': 'login.html'},
		name = 'mbu_login')
)

# Scout URLS
urlpatterns += patterns(
        '',
	url(r'^scout/register/', 'mbu.views.register_scout', name = 'register_scout')
)
