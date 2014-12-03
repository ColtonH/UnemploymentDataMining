from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import TemplateView

from dajaxice.core import dajaxice_autodiscover, dajaxice_config
dajaxice_autodiscover()
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from django.contrib.sitemaps.views import sitemap

from .sitemaps import StaticViewSitemap

sitemaps = {
    'static': StaticViewSitemap,
}


urlpatterns = patterns('',
    url(r'^grappelli/', include('grappelli.urls')), # grappelli URLS
    url(r'^admin/',  include(admin.site.urls)), # admin site
    url(r'^visualization/', include('visualization.urls')),  
    url(r'^data/', include('data.urls')),
    url(r'^data_mining/', include('data_mining.urls')),    
    url(r'^$', TemplateView.as_view(template_name='index.html'),name='home'),
    url(dajaxice_config.dajaxice_url, include('dajaxice.urls')),
    url(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps},name='django.contrib.sitemaps.views.sitemap')
)


urlpatterns += staticfiles_urlpatterns()
