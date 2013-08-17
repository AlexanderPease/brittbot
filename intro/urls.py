from django.conf.urls import patterns, include, url
from intro import views

urlpatterns = patterns('brittbot.views',
    url(r'^$', views.index, name='index'),
    url(r'^response/(?P<intro_id>[0-9]+)/$', views.response, name='response'),
)