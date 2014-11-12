from django.conf.urls import patterns, url
import views

urlpatterns = patterns('', url(r'^clouditem/$', views.cloudItem),url(r'^clouditem/(\d+)/$',views.showCloudItem))

