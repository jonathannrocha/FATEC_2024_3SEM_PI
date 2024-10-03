from django.shortcuts import render, get_object_or_404
from user.models import Perfil, User
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
    
def marcarMentoria(request, cpf):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Usuário não autenticado.'}, status=401)    
    if request.user.typeUser != 'mentorado':
        return JsonResponse({'error': 'Apenas mentorados podem marcar mentorias.'}, status=403)
    mentor = get_object_or_404(User, cpf=cpf, typeUser='mentor')
    try:
        perfil_mentor = Perfil.objects.get(cpf=mentor.cpf)
    except Perfil.DoesNotExist:
        return JsonResponse({'error': 'Perfil do mentor não encontrado.'}, status=404)
    if not perfil_mentor.horariosDisponiveis:
        return JsonResponse({'error': 'O mentor não tem horários disponíveis.'}, status=400)
    return JsonResponse({'success': f'Mentoria marcada com o mentor {mentor.nome}.'})