from django.urls import path
from .views import *

urlpatterns = [
    path('', MainProfile, name='account-home'),
]
