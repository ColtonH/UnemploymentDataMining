from django.conf.urls import patterns, url
from . import views

urlpatterns = patterns('',
    url(r'^$', views.index),
    url(r'^single/unemployment$', views.unemployment_timesseries),
    url(r'^kmeans$', views.kmeans_test),
    url(r'^unemployment_map$',views.unemployment),
    url(r'^unemployment/json$',views.unemployment_json),
    
    # url(r'^articles/(?P<year>\d{4})/$', views.year_archive),
    # url(r'^articles/(?P<year>\d{4})/(?P<month>\d{2})/$', views.month_archive),
    # url(r'^articles/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/$', views.article_detail),
)