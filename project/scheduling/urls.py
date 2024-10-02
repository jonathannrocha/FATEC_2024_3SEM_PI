from django.urls import path
from . import views

urlpatterns = [
    path('horarios/<str:cpf>/',views.viewHorarios, name='viewHorarios')
]