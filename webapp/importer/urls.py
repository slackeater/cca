from django.conf.urls import patterns, url
from importer import views

urlpatterns = patterns('', url(r'^importer/(\d+)/$', views.importer))
