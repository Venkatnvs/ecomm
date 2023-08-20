from django.urls import path
from .views import *

urlpatterns = [
    path('chat/', ChatBotIndex, name='chatbot_fullpg_index'),
    path('chat/api/test/', test_snippets, name='chatbot_fullpg_index_test'),
    path('chat/test/', test_snippets2, name='chatbot_fullpg_index_test2'),
    path('api/chat_responce/', chatbot_api, name='chatbot_fullpg_api'),
    path('', index, name='index'),
    path('<str:room_name>/', room, name='room'),
]