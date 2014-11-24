from django.conf.urls import patterns, url
from . import views

urlpatterns = patterns('',
    url(r'^$', views.index),
    # TIMESERIES
    url(r'^timeseries/unemployment$', views.timeseries_unemployment),

    url(r'^timeseries/natality/num_births$', views.timeseries_natality,{'variable':"num_births"}),
    url(r'^timeseries/natality/birth_rate$', views.timeseries_natality,{'variable':"birth_rate"}),
    url(r'^timeseries/natality/fertility_rate$', views.timeseries_natality,{'variable':"fertility_rate"}),

    url(r'^timeseries/mortality/num_deaths$', views.timeseries_mortality,{'variable':"num_deaths"}),
    url(r'^timeseries/mortality/crude_rate$', views.timeseries_mortality,{'variable':"crude_rate"}),

    # END TIMESERIES

    # MAPS

    # url(r'^map/natality$',views.natality_map),
    # url(r'^map/mortality$',views.natality_map),
    url(r'^map/unemployment$',views.map_unemployment),

    # END MAPS
    url(r'^playground/kmeans$', views.kmeans_test),
    
    
    # url(r'^articles/(?P<year>\d{4})/$', views.year_archive),
    # url(r'^articles/(?P<year>\d{4})/(?P<month>\d{2})/$', views.month_archive),
    # url(r'^articles/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/$', views.article_detail),
)