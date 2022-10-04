from django.urls import path
from .views import feedimport, BlogMain, BlogDetail, BlogCreate

urlpatterns= [
    path('', BlogMain.as_view(), name='blog-main'),
    path('add-post/', BlogCreate.as_view(), name='blog-create'),
    path('d/<int:pk>', BlogDetail.as_view(), name='blog-detail'),
    path('import/', feedimport, name='blog-import'),
]