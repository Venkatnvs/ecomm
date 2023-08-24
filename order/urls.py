from django.urls import path
from .views import *
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('update-cart',UpdateCartItems, name='order_cart_update'),
    path('get-item-amz',GetItemsFromAmazon, name='getitemamz'),
    path('pro-amt',try_amas, name='proam-try'),
    path('order-process/',ProcessOrder, name='order-process'),
]
