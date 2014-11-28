from django.conf.urls import patterns, url
from . import views
from data.models import UnemploymentByStateMonthly, NatalityByStateYearly, MortalityByStateYearly

urlpatterns = patterns('',
    url(r'^$', views.index),
    # CLUSTERING
    url(r'clustering/unemployment_vs_births', views.clustering_unemp_births,{'model':NatalityByStateYearly,'variable':"num_births"}),

)
