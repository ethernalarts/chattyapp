import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.utils import timezone


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # self.id = self.scope['url_route']['kwargs']
        self.user = self.scope['user']
        self.chat_room_name = 'General'

        # join room group
        await self.channel_layer.group_add(
            self.chat_room_name,
            self.channel_name
        )

        # accept connection
        await self.accept()

    async def disconnect(self, close_code):
        # leave chat room
        await self.channel_layer.group_discard(
            self.chat_room_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        # send message to room group
        await self.channel_layer.group_send(
            self.chat_room_name,
            {
                'type': 'chat_message',
                'message': message,
                'user': self.user.username,
                'datetime': timezone.now().isoformat(),
            }
        )

    # receive message from room group
    async def chat_message(self, event):
        # send message to WebSocket
        await self.send(text_data=json.dumps(event))
