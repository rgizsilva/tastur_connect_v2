from django.db import models
from clientes.models import Cliente
from parceiros.models import Parceiro
import uuid

class Reserva(models.Model):
    numero_reserva = models.CharField(max_length=10, primary_key=True, default=uuid.uuid4().hex[:10])
    nome_cliente = models.CharField(max_length=100)
    data_entrada = models.DateField(auto_now_add=True)
    cpf_cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='reservas')
    colaborador_responsavel = models.CharField(max_length=100)
    nome_fantasia = models.CharField(max_length=100)
    cnpj = models.ForeignKey(Parceiro, on_delete=models.CASCADE, related_name='reservas')
    origem = models.CharField(max_length=100)
    destino = models.CharField(max_length=100)
    data_ida = models.DateField()
    data_volta = models.DateField()
    comentarios_adicionais = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"Reserva {self.numero_reserva} - {self.nome_cliente}"
    
    def save(self, *args, **kwargs):
        if not self.numero_reserva:
            self.numero_reserva = uuid.uuid4().hex[:10]
        super().save(*args, **kwargs)
