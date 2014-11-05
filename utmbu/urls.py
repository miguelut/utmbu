from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'utmbu.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    # url(r'^$', auth_views.login, {'template_name':'mbu/login.html'})
)

urlpatterns += patterns(
	#'django.contrib.auth.views',
	'',

	url(r'^login/', 'mbu.views.login_user',
		#{'template_name': 'login.html'},
		name = 'mbu_login')
)