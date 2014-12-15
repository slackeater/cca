from django.conf.urls import patterns, url
from browserfiles import views

urlpatterns = patterns('', url(r'^browserfiles/(\d+)/$', views.browserfiles))
