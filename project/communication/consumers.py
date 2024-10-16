from channels.generic.websocket import AsyncWebsocketConsumer
import json
from communication.models import Room
from datetime import datetime
import pytz
import logging

class ChatConsumer(AsyncWebsocketConsumer):
    
    async def connect(self):
        self.salaId = self.scope['url_route']['kwargs']['salaId']
        self.room_group_name = f'chat_{self.salaId}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        
        text_data_json = json.loads(text_data)
        message = text_data_json['mensagem']
        sender = text_data_json['remetente']

        self.save_message(sender, message)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'mensagem': message,
                'remetente': sender
            }
        )

    async def chat_message(self, event):
        
        message = event['mensagem']
        sender = event['remetente']

        await self.send(text_data=json.dumps({
            'mensagem': message,
            'remetente': sender
        }))

    def save_message(self, sender, message):
        try:
            print(f"Tentando salvar mensagem de {sender} na sala {self.salaId}")
            
            room = Room.objects.get(salaId=self.salaId)
            
            timestamp = datetime.now(pytz.timezone('America/Sao_Paulo')).isoformat()
            
            nova_mensagem = {
                'sender': sender,
                'content': message,
                'timestamp': timestamp
            }

            print(f"Mensagem formatada: {nova_mensagem}")
            
            room.mensagens.append(nova_mensagem)
            room.save()
            print(f"Mensagem salva com sucesso na sala {self.salaId}")
        
        except Room.DoesNotExist:
            print(f"Erro: Sala com salaId {self.salaId} não encontrada.")
        
        except Exception as e:
            logging.error(f"Erro ao salvar a mensagem no MongoDB: {str(e)}")
            print(f"Erro ao salvar a mensagem no MongoDB: {str(e)}")
