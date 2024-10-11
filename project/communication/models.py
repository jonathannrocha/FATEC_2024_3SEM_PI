from mongoengine import Document, StringField, DateTimeField, ListField
import random
import string
from datetime import datetime

# Create your models here.

def uniqueKeySalaID():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=8))

class Room(Document):
    cpfMentor = StringField(required=True)
    cpfMentorado = StringField(required=True)
    salaId = StringField(default=uniqueKeySalaID, unique=True)
    mensagens = ListField(StringField())
    
    def __str__(self):
        return f"Sala: {self.salaId} - Mentor: {self.cpfMentor} - Mentorado: {self.cpfMentorado}"

class Message(Document):
    room = StringField(required=True)
    sender = StringField(required=True)
    content = StringField(required=True)
    timestamp = DateTimeField(default=datetime.utcnow)
    
    def __str__(self):
        return f"{self.sender}: {self.content} at {self.timestamp}"