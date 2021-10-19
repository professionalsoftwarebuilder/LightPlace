# chat/consumers.py
from django.contrib.auth import get_user_model
from asgiref.sync import async_to_sync
import json
from channels.generic.websocket import WebsocketConsumer
from .models import Message, Chat
import logging

User = get_user_model()

class ChatConsumer(WebsocketConsumer):


    def fetch_messages(self, data):
        print('afetch')

        chatGroupNm = data['chatGroupNm']
        messages = Message.last_10_messages(chatGroupNm)
        print('bfetch')
        if messages:
            content = {
                'command': 'messages',
                'messages': self.messages_to_json(messages)
            }
            print('send last 10 messages')
            self.send_message(content)
        else:
            print('no messages')


    # Create Json version of messages
    def messages_to_json(self, messages):
        result = []
        for message in messages:
            result.append(self.message_to_json(message))
        # result is a list of json objects
        return result


    def message_to_json(self, message):
        # Hier wordt blijkbaar steeds een Json obj aangemaakt
        return {
            'author': message.msg_Author.username,
            'content': message.msg_Content,
            'timestamp': str(message.msg_TimeStamp)
        }


    def new_message(self, data):
        print('new message')
        # Get sender from data
        author = data['from']
        print(author)
        chatGroupNm = data['chatGroupNm']
        print(chatGroupNm)
        chatGroup = Chat.objects.get(cht_Name=chatGroupNm)
        print('Chatgroup opgehaald')
        global User
        author_user = User.objects.get(username=author)
        message = Message.objects.create(msg_Author=author_user, msg_ChatGroup=chatGroup, msg_Content=data['message'])
        print('message created in database')
        content = {
            'command': 'new_message',
            'message': self.message_to_json(message)
        }
        return self.send_chat_message(content)


    # Moet hier staan (hoisting probleem)
    commands = {
        'fetch_messages': fetch_messages,
        'new_message': new_message
    }


    def connect(self):
        print('in connect')
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        print(self.room_group_name)
        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()


    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )


    # Receive message from WebSocket
    def receive(self, text_data):
        data = json.loads(text_data)
        print('recieve')
        # Hier word afh v command een functie aangeroepen (fetch_m.. of new_m..)
        self.commands[data['command']](self, data)


    def send_chat_message(self, message):
        # Send message to room group
        print('send_msg_around')
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )


    def send_message(self, message):
        self.send(text_data=json.dumps(message))


    # Receive message from room group
    def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps(message))
