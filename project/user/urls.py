from django.urls import path
from . import views

urlpatterns = [
    path('',views.index, name='index'),
    path('cadastro/',views.cadastrarUsuario, name="cadastro"),
    path('login/',views.user_login, name='user_login'),
    path('logout/', views.logoutView, name='logout'),


    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashbord/conta', views.dashbord_conta, name= 'dashbord_conta')
]