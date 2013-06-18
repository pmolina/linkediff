from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'main.views.home', name='home'),
	url(r'^login/?$', 'main.views.oauth_login', name="oauth_login"),
	url(r'^logout/?$', 'main.views.oauth_logout', name="oauth_logout"),
	url(r'^login/authenticated/?$', 'main.views.oauth_authenticated', name="oauth_authenticated"),
    url(r'^admin/', include(admin.site.urls)),
)
