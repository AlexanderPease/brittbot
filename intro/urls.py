from django.conf.urls import patterns, include, url
from intro import views

urlpatterns = patterns('companies.views',
    url(r'^$', views.index, name='index'),
)