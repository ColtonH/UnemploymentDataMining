from django.conf.urls import patterns, url
from . import views
from data.models import UnemploymentByStateMonthly, NatalityByStateYearly, MortalityByStateYearly

urlpatterns = patterns('',
    url(r'^$', views.index, name='visualization'),
    # TIMESERIES
    url(r'^timeseries/unemployment$', views.timeseries_unemployment, name='visualization/timeseries/unemployment'),

    url(r'^timeseries/natality/num_births$', views.timeseries_natality,{'variable':"num_births"}, name='visualization/timeseries/number_of_births'),
    url(r'^timeseries/natality/birth_rate$', views.timeseries_natality,{'variable':"birth_rate"}, name='visualization/timeseries/birth_rate'),
    url(r'^timeseries/natality/fertility_rate$', views.timeseries_natality,{'variable':"fertility_rate"}, name='visualization/timeseries/fertility_rate'),

    url(r'^timeseries/mortality/num_deaths$', views.timeseries_mortality,{'variable':"num_deaths"}, name='visualization/timeseries/number_of_deaths'),
    url(r'^timeseries/mortality/crude_rate$', views.timeseries_mortality,{'variable':"crude_rate"}, name='visualization/timeseries/crude_rate'),

    # END TIMESERIES

    # MAPS
    url(r'^map/unemployment$',views.map_variable,{'variable':'value','model':UnemploymentByStateMonthly}, name='visualization/map/unemployment'),

    url(r'^map/natality/num_births$',views.map_variable,{'variable':'num_births','model':NatalityByStateYearly}, name='visualization/map/number_of_births'),
    url(r'^map/natality/birth_rate$',views.map_variable,{'variable':'birth_rate','model':NatalityByStateYearly}, name='visualization/map/birth_rate'),
    url(r'^map/natality/fertility_rate$',views.map_variable,{'variable':'fertility_rate','model':NatalityByStateYearly}, name='visualization/map/fertility_rate'),

    url(r'^map/mortality/num_deaths$',views.map_variable,{'variable':'num_deaths','model':MortalityByStateYearly}, name='visualization/map/number_of_deaths'),
    url(r'^map/mortality/crude_rate$',views.map_variable,{'variable':'crude_rate','model':MortalityByStateYearly}, name='visualization/map/crude_rate'),
    
    # END MAPS
    url(r'^playground/kmeans$', views.kmeans_test),
	
	url(r'^playground/association_mortality$',views.association_mortality),
    
    
    # url(r'^articles/(?P<year>\d{4})/$', views.year_archive),
    # url(r'^articles/(?P<year>\d{4})/(?P<month>\d{2})/$', views.month_archive),
    # url(r'^articles/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/$', views.article_detail),
)