from django.db import models
from clientes.models import Cliente
from parceiros.models import Parceiro
import uuid
from django.utils import timezone

class Reserva(models.Model):
    numero_reserva = models.CharField(max_length=10, primary_key=True, default=uuid.uuid4().hex[:10])
    nome_cliente = models.CharField(max_length=100)
    data_entrada = models.DateField(default=timezone.now)
    cpf_cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='reservas')
    colaborador_responsavel = models.CharField(max_length=100)
    nome_fantasia = models.CharField(max_length=100)
    cnpj = models.ForeignKey(Parceiro,null=True,on_delete=models.CASCADE, related_name='reservas')
    origem = models.CharField(max_length=100)
    destino = models.CharField(max_length=100)
    data_ida = models.DateField()
    data_volta = models.DateField()
    comentarios_adicionais = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"Reserva {self.numero_reserva} - {self.nome_cliente}"

    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  
