from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^new_order/$', views.new_order, name='new_order'),
    url(r'^non_delivered/$', views.nondelivered, name='non_delivered'),
    url(r'^seed_file/$', views.seedfile, name='seed_file'),
    url(r'^reports_delivered/$', views.reportsdelivered, name='reports_delivered'),	
]
