from django.urls import path
from chat.consumers import ChatConsumer
from notification.consumers import NotificationConsumer
from voice.consumers import VoiceConsumer

websocket_urlpatterns = [
    path('ws/chat/<room_name>/', ChatConsumer.as_asgi()),
    path('ws/notification/<user_name>/', NotificationConsumer.as_asgi()),
    path('ws/voice/v/<user_token>/', VoiceConsumer.as_asgi()),
]