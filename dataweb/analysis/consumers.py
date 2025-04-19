# analysis/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer

class TrainLogConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = f'train_logs_{self.scope["user"].id}'
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def send_log(self, event):
        await self.send(text_data=json.dumps({"log": event["message"]}))
