from django.urls import path
from .views import *

urlpatterns = [
    path('c/<slug>', CategoriePage, name='st-cate-index'),
    path('s/<slug>', SubCategoriePage, name='st-subcate-index'),
]
