from django.conf.urls import patterns, url
import views

urlpatterns = patterns('', url(r'^comparator/(\d+)/(\d+)/$', views.comparatorView))

