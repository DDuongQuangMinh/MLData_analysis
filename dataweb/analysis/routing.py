# analysis/routing.py
from django.urls import path
from .consumers import TrainLogConsumer

websocket_urlpatterns = [
    path("ws/train-logs/", TrainLogConsumer.as_asgi()),
]
