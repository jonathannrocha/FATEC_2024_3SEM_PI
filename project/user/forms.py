from django import forms
from .models import User
from django.forms import PasswordInput

class UserForm(forms.ModelForm):
    senha = forms.CharField(widget=PasswordInput(), max_length=128)

    class Meta:
        model = User
        fields = ['nome', 'cpf', 'senha', 'gmail', 'telefone', 'dataNascimento', 'typeUser']
        widgets = {
            'dataNascimento': forms.DateInput(attrs={'type': 'date'}),
        }
        
class LoginForm(forms.Form):
    cpf = forms.CharField(max_length=11, label="CPF")
    senha = forms.CharField(widget=forms.PasswordInput, label="Senha")
    
    
class PerfilForm(forms.Form): # MongoDB
    nome = forms.CharField(max_length=128, label='nome')
    sobre = forms.CharField(max_length=255, label='sobre')
    nivelExperiencia = forms.CharField(max_length=255, label='nivelExperiencia')
    nivel = forms.CharField(max_length=298, label='nivel')
    certificacoes = forms.CharField(max_length=221, label="certificacoes")
    habilidades = forms.CharField(max_length=211, label='habilidades')
    redesSocias = forms.CharField(max_length=100,label='redesSocias')