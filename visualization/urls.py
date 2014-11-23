from django.conf.urls import patterns, url
from . import views

urlpatterns = patterns('',
    url(r'^$', views.index),
    url(r'^timeseries/unemployment$', views.timeseries_unemployment),
    # url(r'^timeseries/natality$', views.timeseries_natality),
    # url(r'^timeseries/mortality$', views.timeseries_mortality),

    # url(r'^map/natality$',views.natality_map),
    # url(r'^map/mortality$',views.natality_map),
    url(r'^map/unemployment$',views.map_unemployment),

    url(r'^playground/kmeans$', views.kmeans_test),
    
    
    # url(r'^articles/(?P<year>\d{4})/$', views.year_archive),
    # url(r'^articles/(?P<year>\d{4})/(?P<month>\d{2})/$', views.month_archive),
    # url(r'^articles/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/$', views.article_detail),
)