from django.conf.urls import patterns, url
import views

urlpatterns = patterns('', url(r'^google/(\d+)/(\d+)/$', views.googleView),url(r'^dropbox/(\d+)/(\d+)/$', views.dropboxView))

