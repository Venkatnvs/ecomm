from django.urls import path
from store.admin_views import *

urlpatterns = [
    path('', main, name='admin-home'),
    path('ck/', ckeditor, name='admin-ck'),
    path('category-list/', CategoryListview.as_view(), name='admin-categorylist'),
    path('category-create/', CategoryCreate.as_view(), name='admin-categorycreate'),
    path('category-update/<slug:pk>', CategoryUpdate.as_view(), name='admin-categoryupdate'),
    path('subcategory-list/', SubCategoryListview.as_view(), name='admin-subcategorylist'),
    path('subcategory-create/', SubCategoryCreate.as_view(), name='admin-subcategorycreate'),
    path('subcategory-update/<slug:pk>', SubCategoryUpdate.as_view(), name='admin-subcategoryupdate'),
    path('seller-user-list/', SellerUserListview.as_view(), name='admin-seller-userlist'),
    path('seller-user-create/',SellerUserCreate.as_view(), name='admin-seller-usercreate'),
    path('seller-user-update/<slug:pk>', SellerUserUpdate.as_view(), name='admin-seller-userupdate'),
    path('product-create/',ProductCreateView.as_view(), name='admin-productcreate'),
    path('product-list/', ProductsListview.as_view(), name='admin-productlist'),
    path('product-update/<slug:pk>', ProductsUpdate.as_view(), name='admin-productupdate'),
]