from django.shortcuts import render, redirect
from .forms import UserForm, LoginForm, PerfilForm
from django.contrib.auth import login as auth_login, authenticate
from django.contrib import messages
from .models import User, Perfil
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.contrib.auth import logout
from mongoengine import connect
from database.db import connectMongoDB
from mongoengine.queryset.visitor import Q

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
                messages.success(request, "Login realizado com sucesso.")
                return redirect('user:dashboard')
            else:
                messages.error(request, 'CPF ou senha inválidos.')
        else:
            messages.error(request, 'Erro na validação do formulário.')
    else:
        form = LoginForm()

    return render(request, 'user/login.html', {'form': form})

def cadastrarUsuario(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['senha'])
            user.save()

            perfil = Perfil(
                iduser=user.iduser,
                nome=user.nome,
                sobre='',
                nivelExperiencia='',
                certificacoes=[],
                habilidades=[],
                redesSociais={}
            )
            perfil.save()
            messages.success(request, "Usuário cadastrado com sucesso!")
            return redirect('user:index')
        else:
            messages.error(request, "Erro no cadastro. Verifique os dados.")
    else:
        form = UserForm()

    return render(request, 'user/cadastro.html', {'form': form})

def contato(request):
    return render(request, 'contato.html')

def novidades(request):
    return render(request, 'novidades.html')

def index(request):
    return render(request, 'user/index.html')

@login_required 
def dashboard(request):
    logged_in_user = request.user
    return render(request, 'user/dashboardHome.html', {'user': logged_in_user})

@login_required
def dashboardConta(request):
    logged_in_user = request.user
    perfil = Perfil.objects.get(cpf=logged_in_user.cpf)

    if request.method == 'POST':
        body = request.POST
        dados = body.dict()
        formpefil = PerfilForm(body)

        if formpefil.is_valid():
            perfil.nome = dados['nome']
            perfil.sobre = dados['sobre'] 
            perfil.nivelExperiencia = dados['nivelExperiencia']. capitalize()
            perfil.redesSociais = { 
                'facebook': dados['facebook'], 
                'x':dados['x'], 
                'instagram': dados['instagram'], 
                'linkedIn': dados['linkedIn'] 
            }   

            perfil.habilidades = body.getlist('habilidades')
           
            perfil.horariosDisponiveis = [ 
                { 'horarioInicial': dados['horaInicio'], 'horarioFinal': dados['horaFinal'] },
               {  'atende': body.getlist('diasAtendimento') }
            ]

            logged_in_user.nome =  dados['nome']
            logged_in_user.save()
           
            perfil.save()

    formPerfil = PerfilForm(
        initial={ 
            'nome': perfil.nome,
            'sobre': perfil.sobre, 
            'nivelExperiencia':   perfil.nivelExperiencia,
            'facebook':   perfil.redesSociais['facebook'] if 'facebook' in perfil.redesSociais else "", 
            'instagram':  perfil.redesSociais['instagram'] if 'instagram' in perfil.redesSociais else "" ,
            'x': perfil.redesSociais['x'] if 'x' in perfil.redesSociais else "" ,
            'linkedIn': perfil.redesSociais['linkedIn'] if 'linkedIn' in perfil.redesSociais else "",
            'habilidades': perfil.habilidades,
            'diasAtendimento':  perfil.horariosDisponiveis[1].get('atende') if len(perfil.horariosDisponiveis) > 0 else "" ,
            'horaInicio': perfil.horariosDisponiveis[0].get('horarioInicial') if len(perfil.horariosDisponiveis) > 0 else "",
            'horaFinal' :perfil.horariosDisponiveis[0].get('horarioFinal')if len(perfil.horariosDisponiveis) > 0 else ""
             
        }
    )
        
    return render(
        request, 'user/dashboardConta.html', 
        {
            'formPerfil': formPerfil, 
            'user': logged_in_user, 
            'perfil': perfil,
        }
    )

@login_required
@never_cache
def mentorProfile(request):
    logged_in_user = request.user
    
    perfil = Perfil.objects( ) 
    
    valor_pesquisa = request.POST.get('search_query')
    if valor_pesquisa != None:
        perfil = Perfil.objects.filter(
           Q(nome__icontains=valor_pesquisa) 
        )

    return render(request, 'user/listProfile.html', {'user': logged_in_user, 'perfis': perfil})

@login_required
@never_cache
def dashboardChat(request):
    logged_in_user = request.user
    return render(request, 'communication/dashboardChat.html', {'user': logged_in_user})

@login_required
@never_cache
def agendamentoSemanal(request):
    logged_in_user = request.user
    return render(request, 'scheduling/agendamentoSemanal.html', {'user': logged_in_user})

@login_required
@never_cache
def agendamentoMensal(request):
    logged_in_user = request.user
    return render(request, 'scheduling/agendamentoMes.html', {'user': logged_in_user})

@login_required
@never_cache
def logoutView(request):
    logout(request)
    messages.success(request, "Você foi desconectado com sucesso.")
    return redirect('user:user_login')

def profileMentor(request,  cpf):
    print(cpf)
    return render(request, 'user/profile.html')
