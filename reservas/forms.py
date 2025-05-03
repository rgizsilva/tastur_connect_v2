# reservas/forms.py
from django import forms
from .models import Reserva
from clientes.models import Cliente
from parceiros.models import Parceiro
from django_select2 import forms as s2forms # Importar o widget

class ClienteWidget(s2forms.ModelSelect2Widget):
    search_fields = [
        "cpf_cliente__icontains",
        "nome_completo__icontains",
    ]

class ParceiroWidget(s2forms.ModelSelect2Widget):
    search_fields = [
        "cnpj__icontains",
        "nome_fantasia__icontains",
    ]

class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        exclude = (
            'numero_reserva', 
            'data_entrada', 
            'nome_cliente', 
            'nome_fantasia', 
            'colaborador_responsavel'
        )
        widgets = {
            'data_ida': forms.DateInput(attrs={'type': 'date'}),
            'data_volta': forms.DateInput(attrs={'type': 'date'}),
            'comentarios_adicionais': forms.Textarea(attrs={'rows': 4}),
            # Usar os widgets do Select2
            'cpf_cliente': ClienteWidget,
            'cnpj': ParceiroWidget,
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cpf_cliente'].label = "Cliente (Digite CPF ou Nome para buscar)"
        self.fields['cpf_cliente'].queryset = Cliente.objects.all() 
        self.fields['cpf_cliente'].required = True 

        self.fields['cnpj'].label = "Parceiro (Digite CNPJ ou Nome Fantasia para buscar - Opcional)"
        self.fields['cnpj'].queryset = Parceiro.objects.all() 
        self.fields['cnpj'].required = False 


class ConsultaReservaForm(forms.Form):
    numero_reserva = forms.CharField(max_length=10, required=False, label='Número da Reserva')
    cpf_cliente = forms.CharField(max_length=14, required=False, label='CPF do Cliente')

