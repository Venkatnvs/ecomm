from django.urls import path
from chat.consumers import ChatConsumer
from notification.consumers import NotificationConsumer

websocket_urlpatterns = [
    path('ws/chat/<room_name>/', ChatConsumer.as_asgi()),
    path('ws/notification/<user_name>/', NotificationConsumer.as_asgi()),
]