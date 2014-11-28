from django.conf.urls import patterns, url
from . import views
from data.models import UnemploymentByStateMonthly, NatalityByStateYearly, MortalityByStateYearly

urlpatterns = patterns('',
    url(r'^$', views.index),
    # CLUSTERING
    url(r'clustering/unemployment_vs_births', views.clustering_unemp_var,{'model':NatalityByStateYearly,'variable':"num_births"}),
    url(r'clustering/unemployment_vs_deaths', views.clustering_unemp_var,{'model':MortalityByStateYearly,'variable':"num_deaths"}),

)
