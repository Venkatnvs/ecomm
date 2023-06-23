from django.urls import path
from store import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('', views.main, name='home'),
    path('cart/', views.Cart, name='cart'),
    path('checkout/', views.Checkout, name='checkout'),
    path('product/<slug>', views.ProductDetails, name='productdetails'),
    path('state-dist', csrf_exempt(views.state_dist), name='state-dist'),
]
