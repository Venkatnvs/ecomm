from django.urls import path
from .views import *

urlpatterns= [
    path('', main, name='voice-main'),
    path('v/', dgdgdgdgd, name='voice-main2'),
    path('v/text/', json_voice, name='voice-main3'),
    path('v/text2/', json_voice2, name='voice-main6'),
    path('v/wish', wishing, name='voice-main4'),
    path('v/redirect', redirecturl, name='voice-main5'),
]