from django.conf.urls import patterns, url
import views

urlpatterns = patterns('', url(r'^timeliner/(\d+)/(\d+)/$', views.showTimeline))

