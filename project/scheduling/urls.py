from django.urls import path
from . import views

app_name = 'agendamentos'

urlpatterns = [
    path('horarios/<str:cpf>/',views.viewHorarios, name='viewHorarios'),
    path('marcarMentoria/<str:cpf>/', views.marcarMentoria, name='marcarMentoria'),
]