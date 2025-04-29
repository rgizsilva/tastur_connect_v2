from django import forms
from .models import Reserva
from clientes.models import Cliente
from parceiros.models import Parceiro

class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = '__all__'
        widgets = {
            'data_ida': forms.DateInput(attrs={'type': 'date'}),
            'data_volta': forms.DateInput(attrs={'type': 'date'}),
            'comentarios_adicionais': forms.Textarea(attrs={'rows': 4}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cpf_cliente'].queryset = Cliente.objects.all()
        self.fields['cnpj'].queryset = Parceiro.objects.all()

class ConsultaReservaForm(forms.Form):
    numero_reserva = forms.CharField(max_length=10, required=False, label='Número da Reserva')
    cpf_cliente = forms.CharField(max_length=14, required=False, label='CPF do Cliente')
