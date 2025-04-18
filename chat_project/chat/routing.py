from django.urls import re_path
from .interface.channels.consumers import ChatConsumer

websocket_urlpatterns = [
    # re_path(r"ws/chat/(?P<room_name>\w+)/$", consumers.ChatConsumer.as_asgi()),
    re_path(r'ws/chat/(?P<room_name>\w+)/$', ChatConsumer.as_asgi()),
]