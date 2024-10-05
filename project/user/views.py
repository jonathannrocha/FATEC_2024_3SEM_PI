from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import UserForm, LoginForm, PerfilForm
from django.contrib.auth import login as auth_login, authenticate, login as auth_login
from django.contrib.auth.hashers import check_password
from django.contrib import messages
from .models import User, Perfil
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.contrib.auth import logout
from mongoengine import connect
from database.db import connectMongoDB

connectMongoDB()

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            cpf = form.cleaned_data.get('cpf')
            senha = form.cleaned_data.get('senha')

            user = authenticate(request, username=cpf, password=senha)

            if user is not None:
                auth_login(request, user)
                print(f"Usuário autenticado: {user}")
                print(f"ID da Sessão após login: {request.session.session_key}")

                if request.session.session_key:
                    print(f"Sessão criada com sucesso: {request.session.session_key}")
                else:
                    print("Sessão não criada corretamente no momento do login")

                return redirect('dashboard')
            else:
                messages.error(request, 'CPF ou senha inválidos.')
        else:
            messages.error(request, 'Erro na validação do formulário.')
    else:
        form = LoginForm()

    print(f"ID da Sessão fora do POST: {request.session.session_key}")
    return render(request, 'user/login.html', {'form': form})

def cadastrarUsuario(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['senha'])
            user.save()

            # Criar o perfil associado ao usuário
            perfil = Perfil(
                cpf=user.cpf,
                nome='',
                sobre='',
                nivelExperiencia='',
                nivel='',
                certificacoes=[],
                habilidades=[],
                redesSociais=[]
            )
            perfil.save()

            messages.success(request, "Usuário cadastrado com sucesso!")
            return redirect('index')
        else:
            print(form.errors)
            messages.error(request, "Erro no cadastro. Verifique os dados.")
    else:
        form = UserForm()

    return render(request, 'user/cadastro.html', {'form': form})

def contato( request ):
    return render( request, 'contato.html')

def novidades( request ):
    return render( request, 'novidades.html')

def index(request):
    return render(request, 'user/index.html')

@login_required
@never_cache
def dashboard(request):
    user = User
    return render(request, 'user/dashbord_home.html', { user: user  })

@login_required
@never_cache
def dashbord_conta(request):
    form = UserForm()
    user = User
    return render( request, 'user/dashbord_conta.html', { 'form':form, user:user  })

def logoutView(request):
    logout(request)
    return redirect('user_login')
