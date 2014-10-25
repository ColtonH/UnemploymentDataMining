from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import TemplateView

urlpatterns = patterns('',
    url(r'^grappelli/', include('grappelli.urls')), # grappelli URLS
    url(r'^admin/',  include(admin.site.urls)), # admin site
    url(r'^visualization/', include('visualization.urls')),    
    url(r'^$', TemplateView.as_view(template_name='index.html'))
)
