from django import forms
from .models import Cliente

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = '__all__'
        widgets = {
            'data_nascimento': forms.DateInput(attrs={'type': 'date'}),
        }

class ConsultaClienteForm(forms.Form):
    cpf = forms.CharField(max_length=14, required=False, label='CPF')
