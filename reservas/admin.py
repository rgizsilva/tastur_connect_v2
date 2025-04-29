from django.contrib import admin
from .models import Reserva

@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = ('numero_reserva', 'nome_cliente', 'cpf_cliente', 'origem', 'destino', 'data_ida', 'data_volta')
    search_fields = ('numero_reserva', 'nome_cliente', 'cpf_cliente__cpf_cliente')
    list_filter = ('data_ida', 'data_volta', 'origem', 'destino')
    date_hierarchy = 'data_entrada'
