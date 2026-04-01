from django.contrib.auth.models import AbstractUser
from django.db import models

class Usuario(AbstractUser):
    username = models.CharField(max_length=150, blank=True, null=True)  # Override to make it optional
    matricula = models.CharField(max_length=20, unique=True)
    nome_completo = models.CharField(max_length=255)
    cpf = models.CharField(max_length=14, unique=True)
    telefone = models.CharField(max_length=20)
    data_nascimento = models.DateField(null=True, blank=True)
    cargo = models.CharField(max_length=20, default='Estagiário')

    USERNAME_FIELD = 'matricula'
    REQUIRED_FIELDS = ['nome_completo', 'cpf', 'email']

    class Meta:
        db_table = 'usuario'

    def __str__(self):
        return self.nome_completo