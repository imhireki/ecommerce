from django.urls import path

from . import consumers


websocket_urlpatterns = [
    path("ws/notifications/broadcast/", consumers.AsyncBroadcastConsumer.as_asgi()),
]
