from django.urls import path
from . import views

urlpatterns = [
    path('',views.index, name='index'),
    path('cadastro/',views.cadastrarUsuario, name="cadastro"),
    path('login/',views.user_login, name='user_login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.logoutView, name='logout'),
]