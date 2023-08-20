from django.urls import path
from .api_views import UserViewSet


urlpatterns = [
    path('', UserViewSet, name='api-auth' ),
]
