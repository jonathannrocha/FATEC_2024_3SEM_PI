from django.shortcuts import render
from user.models import Perfil
from django.http import JsonResponse
from mongoengine import DoesNotExist

# Create your views here.

def viewHorarios(request, cpf):
    try:
        perfil_obj = Perfil.objects.get(cpf=cpf)
        horariosDisponiveis = [h.isoformat() for h in perfil_obj.horariosDisponiveis]
        return JsonResponse({'horariosDisponiveis': horariosDisponiveis}, safe=False)
    except DoesNotExist:
        return JsonResponse({'error': 'Perfil não encontrado'}, status=404)