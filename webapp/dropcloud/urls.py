from django.conf.urls import patterns, url
from dropcloud import views

urlpatterns = patterns('', url(r'^$', views.dropViewer, name='index'),)

