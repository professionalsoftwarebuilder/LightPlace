"""
ASGI config for projChat project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/
"""
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'lightplace.settings.development'

from django.core.asgi import get_asgi_application
django_asgi_app = get_asgi_application()

import chatApp.routing
from .wsgi import *
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter

#django.setup()

application = ProtocolTypeRouter({
    "https": get_asgi_application(),
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            chatApp.routing.websocket_urlpatterns
        )
    ),
})

