from django.urls import path
from .views import video_call, listAllMentor, iniciarChat, chat

app_name = 'communication'

urlpatterns = [
    path('video_call/', video_call, name='video_call'),
    path('test/', listAllMentor, name='listAllMentor'),
    path('iniciarChat/<str:cpfMentor>/', iniciarChat, name='iniciarChat'),
    path('chat/<str:sala_id>/', chat, name='chat'),
]