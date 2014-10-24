from django.conf.urls import patterns, url
from importer import views

urlpatterns = patterns('', url(r'^$', views.importer, name='index'),)
