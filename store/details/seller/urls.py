from django.urls import path
from .views import *

urlpatterns = [
    path('', main, name='seller-index'),
    path('category-list/', CategoryListview.as_view(), name='seller-categorylist'),
    path('category-request/', CategoryRequest.as_view(), name='seller-categoryrequest'),
]
