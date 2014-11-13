from django.conf.urls import patterns, url
import views

urlpatterns = patterns('', url(r'^download/(\d+)/$', views.showTokenDash),url(r'^download/(\d+)/(\d+)/$', views.showDownloadDash))

