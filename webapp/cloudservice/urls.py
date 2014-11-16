from django.conf.urls import patterns, url
import views

urlpatterns = patterns('', url(r'^analyse/(\d+)/(\d+)/$', views.cloudService))

