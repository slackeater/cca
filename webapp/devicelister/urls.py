from django.conf.urls import patterns, url
from devicelister import views

urlpatterns = patterns('', url(r'^devices/(\d+)/(\d+)/$', views.devicelister))
