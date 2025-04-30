# reservas/forms.py
from django import forms
from .models import Reserva
from clientes.models import Cliente
from parceiros.models import Parceiro

class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        # Excluir campos que serão preenchidos na view
        exclude = ('numero_reserva', 'data_entrada', 'nome_cliente', 'nome_fantasia')
        widgets = {
            'data_ida': forms.DateInput(attrs={'type': 'date'}),
            'data_volta': forms.DateInput(attrs={'type': 'date'}),
            'comentarios_adicionais': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['cpf_cliente'].queryset = Cliente.objects.all()
        self.fields['cpf_cliente'].label = "Cliente (Selecione pelo CPF)" 
        self.fields['cpf_cliente'].empty_label = "Selecione um Cliente"

        self.fields['cnpj'].queryset = Parceiro.objects.all()
        self.fields['cnpj'].label = "Parceiro (Selecione pelo CNPJ)" 
        self.fields['cnpj'].empty_label = "Selecione um Parceiro"

        
        self.fields['colaborador_responsavel'].widget = forms.HiddenInput()
        self.fields['colaborador_responsavel'].required = False


class ConsultaReservaForm(forms.Form):
    numero_reserva = forms.CharField(max_length=10, required=False, label='Número da Reserva')
    cpf_cliente = forms.CharField(max_length=14, required=False, label='CPF do Cliente')

