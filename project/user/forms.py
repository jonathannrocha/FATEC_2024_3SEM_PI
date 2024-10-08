from django import forms
from .models import User, Perfil
from django.forms import PasswordInput

class UserForm(forms.ModelForm):
    senha = forms.CharField(widget=PasswordInput(), max_length=128)
 
    class Meta:
        model = User     
        fields = ['nome', 'cpf', 'senha', 'gmail', 'telefone', 'dataNascimento', 'typeUser']
         

        widgets = {
            'nome': forms.TextInput( attrs={'placeholder': 'nome completo'}),
            'cpf': forms.TextInput( attrs={'placeholder': 'cpf'}),
            'gmail': forms.EmailInput( attrs={ 'placeholder': 'emaiil'}),
            'telefone': forms.NumberInput( attrs={ 'placeholder': 'Telefone'}),
            'dataNascimento': forms.DateInput(attrs={'type': 'date'}),
            'typeUser': forms.Select( ),
            'senha': forms.PasswordInput( attrs={'placeholder': 'senha'})
        }

   
        
class LoginForm(forms.Form):
    cpf = forms.CharField(max_length=11, label="CPF")
    senha = forms.CharField(widget=forms.PasswordInput, label="Senha")
    
    
class PerfilForm(forms.Form): # MongoDB
    nome = forms.CharField(  max_length=128, label='Nome Completo')
    sobre = forms.CharField(max_length=255, label='Sobre', widget=forms.Textarea(attrs={"rows":"5"}))
    nivelExperiencia = forms.ChoiceField( choices= [('junior', 'Junior'), ('pleno', 'Pleno'), ( 'senior', 'Sênior')]  )
   
    nome.widget.attrs["class"] = "form-control"
    sobre.widget.attrs["class"] = "form-control"
    nivelExperiencia.widget.attrs["class"] = "form-control"

class PerfilRedesSociais(forms.Form): 
    facebook  = forms.CharField(  max_length=255, label='Facebook ')
    x = forms.CharField(max_length=255, label='X')
    instagram = forms.CharField(max_length=255, label='Instragram')
    linkedIn = forms.CharField(max_length=255, label='LinkedIn')

    facebook.widget.attrs["class"] = "form-control"
    x.widget.attrs["class"] = "form-control"
    instagram.widget.attrs["class"] = "form-control"
    linkedIn.widget.attrs["class"] = "form-control"
 