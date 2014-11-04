from django.conf.urls import patterns, url
from gdrivecloud import views

urlpatterns = patterns('', url(r'^$', views.gdriveViewer, name='index'),)

