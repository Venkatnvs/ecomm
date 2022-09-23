from django.urls import path
from videoplay import views

urlpatterns = [
    path('', views.main, name='videoplay-index'),
]
