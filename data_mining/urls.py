from django.conf.urls import patterns, url
from . import views
from data.models import UnemploymentByStateMonthly, NatalityByStateYearly, MortalityByStateYearly

urlpatterns = patterns('',
    url(r'^$', views.index,name='data-mining'),
    # CLUSTERING
    url(r'clustering/unemployment_vs_births', views.clustering_unemp_var,{'model':NatalityByStateYearly,'variable':"num_births", 'form_url':'/data_mining/clustering/unemployment_vs_births'},name='data-mining/clustering/unemployment_vs_births'),
    url(r'clustering/unemployment_vs_birth_rate', views.clustering_unemp_var,{'model':NatalityByStateYearly,'variable':"birth_rate",'form_url':'/data_mining/clustering/unemployment_vs_birth_rate'},name='data-mining/clustering/unemployment_vs_birth_rate'),
    url(r'clustering/unemployment_vs_fertility_rate', views.clustering_unemp_var,{'model':NatalityByStateYearly,'variable':"fertility_rate",'form_url':'/data_mining/clustering/unemployment_vs_fertility_rate'},name='data-mining/clustering/unemployment_vs_fertility_rate'),

    url(r'clustering/unemployment_vs_deaths', views.clustering_unemp_var,{'model':MortalityByStateYearly,'variable':"num_deaths",'form_url':'/data_mining/clustering/unemployment_vs_deaths'},name='data-mining/clustering/unemployment_vs_deaths'),
    url(r'clustering/unemployment_vs_crude_rate', views.clustering_unemp_var,{'model':MortalityByStateYearly,'variable':"crude_rate",'form_url':'/data_mining/clustering/unemployment_vs_crude_rate'},name='data-mining/clustering/unemployment_vs_crude_rate'),

    #JOHN URLS HERE
	 url(r'association/natality',views.association_natality,name='data-mining/association/statistical/birth_rate'),
	 url(r'association/mortality',views.association_mortality,name='data-mining/association/statistical/crude_rate'),
    #COLTON URLS HERE
    url(r'outliers',views.outliers_crisis,name='data-mining/outliers'),
)
