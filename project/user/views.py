from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import UserForm, LoginForm
from django.contrib.auth import login as auth_login, authenticate, login as auth_login
from django.contrib.auth.hashers import check_password
from django.contrib import messages
from .models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

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
    return render(request, 'login.html', {'form': form})


def cadastrarUsuario(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['senha'])
            user.save()
            return redirect('index')
    else:
        form = UserForm()

    return render(request, 'cadastro.html', {'form': form})

def index(request):
    return render(request, 'index.html')

@login_required
def dashboard(request):
    print(f"Usuário autenticado no dashboard: {request.user.is_authenticated}")
    print(f"ID da Sessão no dashboard: {request.session.session_key}")
    
    if request.user.is_authenticated:
        return HttpResponse(f"Bem-vindo ao dashboard, {request.user.nome}! Sessão ativa: {request.session.session_key}")
    else:
        return HttpResponse("Usuário não autenticado")

def logoutView(request):
    logout(request)
    return redirect('user_login')
