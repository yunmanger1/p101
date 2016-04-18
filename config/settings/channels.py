# -*- coding: utf-8 -*-
from .local import *  # noqa

INSTALLED_APPS += (
    'channels',
)

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "asgi_redis.RedisChannelLayer",
        "CONFIG": {
            "hosts": [env("REDIS_URL", default="redis://localhost:6379")],
        },
        "ROUTING": "config.routing.channel_routing",
    },
}

