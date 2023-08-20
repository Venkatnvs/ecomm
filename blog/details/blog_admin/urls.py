from django.urls import path
from .views import *

urlpatterns= [
    path('', Dashboard, name='blog-admin-main'),
    path('post_create/', BlogCreate.as_view(), name='blog-admin-add_post'),
]