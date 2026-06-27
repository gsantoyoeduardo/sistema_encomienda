import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async


class EncomiendaConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = 'encomiendas_global'
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()
        await self.send(text_data=json.dumps({
            'type': 'connection_established',
            'message': 'Conectado al sistema de notificaciones de encomiendas'
        }))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def receive(self, text_data=None, bytes_data=None):
        if text_data:
            data = json.loads(text_data)
            await self.channel_layer.group_send(
                self.group_name,
                {
                    'type': 'encomienda_message',
                    'message': data.get('message', ''),
                    'data': data
                }
            )

    async def encomienda_message(self, event):
        await self.send(text_data=json.dumps({
            'type': 'encomienda_update',
            'message': event.get('message', ''),
            'data': event.get('data', {})
        }))

    async def encomienda_cambio_estado(self, event):
        await self.send(text_data=json.dumps({
            'type': 'cambio_estado',
            'codigo': event['codigo'],
            'estado_anterior': event['estado_anterior'],
            'estado_nuevo': event['estado_nuevo'],
            'fecha_cambio': event['fecha_cambio'],
            'observacion': event.get('observacion', '')
        }))
