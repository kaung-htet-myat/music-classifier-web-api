from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'stream/listen', consumers.PredictionConsumer.as_asgi()),
]