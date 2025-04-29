from django.contrib import admin
from .models import Cliente

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('cpf_cliente', 'nome_completo', 'telefone', 'cidade', 'possui_reserva')
    search_fields = ('cpf_cliente', 'nome_completo')
    list_filter = ('cidade', 'uf', 'possui_reserva')
