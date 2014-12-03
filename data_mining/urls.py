from django.conf.urls import patterns, url
from . import views
from data.models import UnemploymentByStateMonthly, NatalityByStateYearly, MortalityByStateYearly

urlpatterns = patterns('',
    url(r'^$', views.index,name='data-mining'),
    # CLUSTERING
    url(r'clustering/raw/unemployment_vs_births', views.clustering_unemp_var_raw,{'model':NatalityByStateYearly,'variable':"num_births"},name='data-mining/clustering/unemployment_vs_births'),
    url(r'clustering/raw/unemployment_vs_deaths', views.clustering_unemp_var_raw,{'model':MortalityByStateYearly,'variable':"num_deaths"},name='data-mining/clustering/unemployment_vs_deaths'),
    # url(r'clustering/diff/unemployment_vs_births', views.clustering_unemp_var_diff,{'model':MortalityByStateYearly,'variable':"num_deaths"}),
    # url(r'clustering/diff/unemployment_vs_deaths', views.clustering_unemp_var_diff,{'model':MortalityByStateYearly,'variable':"num_deaths"}),
    #JOHN URLS HERE
	url(r'association/natality',views.association_natality,name='data-mining/association/statistical/birth_rate'),
	url(r'association/mortality',views.association_mortality,name='data-mining/association/statistical/crude_rate'),
    #COLTON URLS HERE
    url(r'outliers',views.outliers_crisis,name='data-mining/outliers'),
)
