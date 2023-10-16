from django.urls import path
from .views import *

urlpatterns = [
    path('', main, name='seller-index'),
    path('sel-seller/', SelectSeller, name='seller-sel-seller'),
    path('category-list/', CategoryListview.as_view(), name='seller-categorylist'),
    path('category-request/', CategoryRequest.as_view(), name='seller-categoryrequest'),
    path('category-request/', CategoryRequest.as_view(), name='seller-categoryrequest'),
    path('staff-user-list/', StaffUserListview.as_view(), name='seller-staff-userlist'),
    path('staff-user-create/', StaffUserCreate.as_view(), name='seller-staff-usercreate'),
    path('product-list/', ProductsListview.as_view(), name='seller-productlist'),
    path('product-add/', ProductCreateView.as_view(), name='seller-productcreate'),
    path('orders-lst', OrdersListview.as_view(), name='seller-orders-lst'),
    path('orders-lst/<trans_id>/', OrdersListDetailsView.as_view(), name='seller-orders-details'),
]
