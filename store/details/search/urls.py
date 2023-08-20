from django.urls import path
from .views import *

urlpatterns = [
    path('s/', HomeSearch, name='st-search-index'),
    path('', SearchResult, name='st-search-mn'),
]
