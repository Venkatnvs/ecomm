from django.urls import path
from .views import *
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path("",MyOrders,name="order-my-orders"),
    path('update-cart',UpdateCartItems, name='order_cart_update'),
    path('get-item-amz',GetItemsFromAmazon, name='getitemamz'),
    path('pro-amt',try_amas, name='proam-try'),
    path('order-process/',ProcessOrder, name='order-process'),
    path('order-handel/<trans_id>',orderHandel, name='order-handel'),
    path('coupon-code/',GetCouponCode, name='order-get-coupon-code'),
    path('cart-bill-total/',GetCarBillingTotal, name='order-cart-bill-total'),
    path('coupon-order-st/',GetCouponExists, name='order-coupon-order-st'),
    path('<order_id>/', order_details, name='order-myorder_details'),
    path('invoice/<order_id>/', generate_invoice, name='order-generate_invoice'),
    path('invoice/pdf/<order_id>/', generate_invoice_pdf, name='order-generate_invoice_pdf'),
]
