# chat/routing.py
from django.conf.urls import url
from django.urls import re_path, path
from chatApp import consumers

websocket_urlpatterns = [
    path('/ws/QQQQ/abc/', consumers.ChatConsumer.as_asgi()),
    re_path(r'^ws/QQQQ/(?P<room_name>\w+)/$', consumers.ChatConsumer.as_asgi()),
    re_path(r'ws/QQQQ/(?P<room_name>\w+)/$', consumers.ChatConsumer.as_asgi()),
    re_path(r'QQQQ/(?P<room_name>\w+)/$', consumers.ChatConsumer.as_asgi()),
    re_path('QQQQ/(?P<room_name>)/$', consumers.ChatConsumer.as_asgi()),
    re_path(r'.*', consumers.ChatConsumer.as_asgi()),
]
