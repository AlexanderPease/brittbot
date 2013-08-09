from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    #url(r'^$', include('companies.urls')),
    url(r'', include('social_auth.urls')), # Twitter user authentication
    #url(r'^login', redirect_to, {'url': '/login/twitter'}), # Twitter user authentication
    url(r'^', include('companies.urls')),
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += staticfiles_urlpatterns()
