from django.urls import path
from envios.consumers import EncomiendaConsumer

websocket_urlpatterns = [
    path('ws/encomiendas/', EncomiendaConsumer.as_asgi()),
]
