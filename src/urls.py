from django.urls import path, re_path
from src import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('', views.main, name='src-home'),
    path('d/', views.main2, name='src-home2'),
    path('d/post', views.post_imd, name='src-home3'),
    path('d/post2', views.post_img2, name='src-home4'),
    path('d/post3', views.post_imd3, name='src-home5'),
    re_path('^d/post4/media/(?P<path>.*)$', views.post_imd4, name='src-home6'),
    path('img', views.getimage, name='src-img'),
]
