from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^new_order/$', views.new_order, name='new_order'),
    url(r'^non_delivered/list/$', views.nondelivered_list, name='non_delivered_list'),
    url(r'^non_delivered/map/$', views.nondelivered_map, name='non_delivered_map'),
    url(r'^seed_file/$', views.seedfile, name='seed_file'),
    url(r'^reports/$', views.reports, name='reports'),	
]
