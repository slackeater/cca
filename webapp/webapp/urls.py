from django.conf.urls import patterns, include, url
from django.contrib import admin
from dajaxice.core import dajaxice_autodiscover, dajaxice_config
dajaxice_autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'webapp.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/$', 'django.contrib.auth.views.login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout',{'next_page': '/login'}),
    url('', include('importer.urls')),
    url('', include('downloader.urls')),
    url('', include('clouditem.urls')),
    url('', include('cloudservice.urls')),
    url('', include('timeliner.urls')),
    url('', include('comparator.urls')),
    url('', include('maps.urls')),
    url('', include('browserfiles.urls')),
    url('', include('tokendash.urls')),
    url('', include('reporter.urls')),
    url('', include('devicelister.urls')),
    url(dajaxice_config.dajaxice_url, include('dajaxice.urls')),
)

