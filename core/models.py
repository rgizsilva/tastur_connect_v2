from django.db import models
from django.contrib.auth.models import User

class Colaborador(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nome_completo = models.CharField(max_length=100)
    telefone = models.CharField(max_length=15)
    
    def __str__(self):
        return self.nome_completo
