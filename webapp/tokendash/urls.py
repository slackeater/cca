from django.conf.urls import patterns, url
import views

urlpatterns = patterns('', url(r'^token/(\d+)/(\d+)/$', views.showTokenSelect),url(r'^token/(\d+)/$', views.showTokenDash))

