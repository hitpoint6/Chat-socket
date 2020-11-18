# chat/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from chat.models import *
from django.utils import timezone, dateformat


class ChatConsumer(AsyncWebsocketConsumer):

    def get_name(self):
        return User.objects.all()[0].username

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()
    
    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        author = text_data_json['author']
        room_id =self.room_name


        timestamp = str(dateformat.format(timezone.now(), 'H:i:s'))

        await self.save_message(message, author, room_id)
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type':'chat_message',
                'message':message,
                'author':author,
                'timestamp':timestamp
            }
        )

    # Receive message from room group
    async def chat_message(self, event):

        message = event['message']
        author = event['author']
        timestamp = event['timestamp']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'author': author,
            'timestamp':timestamp
        }))

    @database_sync_to_async
    def save_message(self, message, author, room_id):
        r = None;       
        participant_obj = Participant.objects.filter(user__username=author)[0]
        try:
            r = Room.objects.get(id=room_id)
        except Room.DoesNotExist:
            r = Room(id=room_id)
            r.save()
        r.participants.add(participant_obj)
        m = Message(author=participant_obj, content=message, room=r)
        m.save()
        m.readers.add(participant_obj)