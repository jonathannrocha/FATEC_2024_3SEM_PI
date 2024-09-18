# forms.py
from django import forms
from .models import User
from django.forms import PasswordInput

class UserForm(forms.ModelForm):
    senha = forms.CharField(widget=PasswordInput(), max_length=11)

    class Meta:
        model = User
        fields = ['nome', 'cpf', 'senha', 'gmail', 'telefone', 'dataNascimento', 'typeUser']
        widgets = {
            'dataNascimento': forms.DateInput(attrs={'type': 'date'}),
        }
        
class LoginForm(forms.Form):
    cpf = forms.CharField(max_length=11, label="CPF")
    senha = forms.CharField(widget=forms.PasswordInput, label="Senha")