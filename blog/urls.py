from django.urls import path
from .views import *

urlpatterns= [
    path("", BlogMain, name="blog-main"),
    path('import/', feedimport, name='blog-import'),
]