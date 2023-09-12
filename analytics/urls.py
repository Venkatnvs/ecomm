from django.urls import path
from .views import *

urlpatterns = [
    path('get-ip-geolocation', get_user_ip_geolocation, name='analytics_ip_geolocation'),
    path('track-page-view', track_page_view, name='analytics_v1'),
    path('get-ip-address', get_user_ip_address, name='analytics_ip_address'),
    path('get-country_graph1', get_country_graph, name='analytics_country_graph1'),
    path('get-country_graph2', get_country, name='analytics_country_graph2'),
]