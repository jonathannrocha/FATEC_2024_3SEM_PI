from django.shortcuts import render, redirect, get_object_or_404
from uuid import uuid4
from user.models import User
from communication.models import Room, Message
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from user.views import user_login
from datetime import datetime
from .forms import MessageForm

# Create your views here.

def video_call(request):
    room_name = str(uuid4())
    return render(request, 'communication/video_call.html', {'room_name': room_name})

def listAllMentor(request):
    listM = User.objects.filter(typeUser='mentorado')
    return render(request, 'communication/dashboardChat.html', {'mentores': listM})

@login_required
def iniciarChat(request, cpfMentor):
    cpfMentorado = request.user.cpf
    SalaE = Room.objects.filter(cpfMentor=cpfMentor, cpfMentorado=cpfMentorado).first()
    if not SalaE:
        newRoom = Room(cpfMentor=cpfMentor, cpfMentorado=cpfMentorado)
        newRoom.save() 
        sala_id = newRoom.salaId
    else:
        sala_id = SalaE.salaId
    return redirect('communication:chat', sala_id=sala_id)

@login_required
def chat(request, sala_id):
    try:
        room = Room.objects.get(salaId=sala_id)
    except Room.DoesNotExist:
        return render(request, '404.html', status=404)

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            mensagem = form.cleaned_data['mensagens']
            nova_mensagem = f"{request.user.cpf}: {mensagem} at {datetime.utcnow()}"
            room.mensagens.append(nova_mensagem)  
            room.save()
            return redirect('communication:chat', sala_id=sala_id)
    else:
        form = MessageForm()

    messages = room.mensagens
    
    return render(request, 'communication/dashboardSala.html', {
        'form': form,
        'room': room,
        'messages': messages
    })