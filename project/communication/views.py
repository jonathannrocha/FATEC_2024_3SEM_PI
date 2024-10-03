from django.shortcuts import render
from uuid import uuid4

# Create your views here.

def video_call(request):
    room_name = str(uuid4())  # Gera um ID único para a sala
    return render(request, 'communication/video_call.html', {'room_name': room_name})
