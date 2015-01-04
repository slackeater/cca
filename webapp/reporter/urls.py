from django.conf.urls import patterns, url
from reporter import views

urlpatterns = patterns('', url(r'^reporter/(\d+)/(\d+)/$', views.generateReport))
