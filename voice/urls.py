from django.urls import path
from .views import *

urlpatterns= [
    path('', main, name='voice-main'),
    path('ws/', ws_main, name='voice-ws-main'),
    path('v/', dgdgdgdgd, name='voice-main2'),
    path('v/yt/<query>/', youtube_songs, name='voice-main2_yt'),
    path('d/yt/<value>/', json_youtube, name='voice-main3_yt'),
    path('v/text/', json_voice, name='voice-main3'),
    path('v/text2/', json_voice2, name='voice-main6'),
    path('v/wish', wishing, name='voice-main4'),
    path('v/redirect', redirecturl, name='voice-main5'),
]