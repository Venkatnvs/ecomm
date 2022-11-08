from django.urls import path
from .views import *

urlpatterns= [
    path('', main, name='video-main'),
    path('v/', main2, name='video-main2'),
    path('v/2/', main3, name='video-main3'),
    path('c/', ctm_play, name='video-ctm'),
]