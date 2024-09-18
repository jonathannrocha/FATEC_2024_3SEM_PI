from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models

class UserManager(BaseUserManager):
    def create_user(self, cpf, senha=None, **extra_fields):
        if not cpf:
            raise ValueError('O CPF é obrigatório')
        user = self.model(cpf=cpf, **extra_fields)
        user.set_password(senha)
        user.save(using=self._db)
        return user

    def create_superuser(self, cpf, senha=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(cpf, senha, **extra_fields)


class User(AbstractBaseUser):
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
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'cpf'
    REQUIRED_FIELDS = ['nome', 'gmail']

    objects = UserManager()

    def __str__(self):
        return self.cpf
