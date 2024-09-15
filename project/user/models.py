from django.db import models

# Create your models here.

class user(models.Model):
    nome = models.CharField(max_length=100)
    cpf = models.CharField(max_length=11, unique=True, primary_key=True)
    gmail = models.EmailField(max_length=100, unique=True)
    telefone = models.CharField(max_length=15)
    dataNascimento = models.DateField(null=True, blank=True)
    typeUser = models.CharField(max_length=10, choices=[
        ('admin', 'Admin'),
        ('mentor', 'Mentor'),
        ('mentorado', 'Mentorado')
    ], default='mentorado')
    
    