from django.conf.urls import patterns, url
from . import views
from data.models import UnemploymentByStateMonthly, NatalityByStateYearly, MortalityByStateYearly

urlpatterns = patterns('',
    url(r'^$', views.index),
    # CLUSTERING
    url(r'clustering/raw/unemployment_vs_births', views.clustering_unemp_var_raw,{'model':NatalityByStateYearly,'variable':"num_births"}),
    url(r'clustering/raw/unemployment_vs_deaths', views.clustering_unemp_var_raw,{'model':MortalityByStateYearly,'variable':"num_deaths"}),
    # url(r'clustering/diff/unemployment_vs_births', views.clustering_unemp_var_diff,{'model':MortalityByStateYearly,'variable':"num_deaths"}),
    # url(r'clustering/diff/unemployment_vs_deaths', views.clustering_unemp_var_diff,{'model':MortalityByStateYearly,'variable':"num_deaths"}),
    #JOHN URLS HERE
	url(r'association/natality',views.association_natality),
    #COLTON URLS HERE
)
