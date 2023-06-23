from django.urls import path
from .views import *
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('update-cart',UpdateCartItems, name='order_cart_update'),
]
