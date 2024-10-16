from django.urls import re_path
from communication import consumers

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<salaId>\w+)/$', consumers.ChatConsumer.as_asgi()),
]
