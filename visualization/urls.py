from django.conf.urls import patterns, url

from . import views

urlpatterns = patterns('',
    url(r'^$', views.index),
    url(r'^single/unemployment$', views.single_unemployment),
    url(r'^kmeans$', views.kmeans_test),
    # url(r'^articles/(?P<year>\d{4})/$', views.year_archive),
    # url(r'^articles/(?P<year>\d{4})/(?P<month>\d{2})/$', views.month_archive),
    # url(r'^articles/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/$', views.article_detail),
)