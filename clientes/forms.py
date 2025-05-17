from django import forms
from .models import Cliente
import re

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = '__all__'
        widgets = {
            'data_nascimento': forms.TextInput(
                attrs={
                    'class': 'form-control datepicker-br',
                    'placeholder': 'DD/MM/AAAA'
                }
            ), 
        }
    def clean_data_nascimento(self):
        data = self.cleaned_data.get('data_nascimento')
        if data and isinstance(data, str):
            try:
                from datetime import datetime
                return datetime.strptime(data, '%d/%m/%Y').date()
            except ValueError:
                raise forms.ValidationError('Data inválida. Use o formato DD/MM/AAAA.')
        return data
        
    def clean_cpf_cliente(self):
        cpf = self.cleaned_data.get('cpf_cliente')
        if cpf:
            cpf_sem_mascara = re.sub(r'\D', '', cpf)  
            return cpf_sem_mascara
        return cpf

class ConsultaClienteForm(forms.Form):
    cpf = forms.CharField(max_length=14, required=False, label='CPF')

    def clean_cpf(self):
        cpf = self.cleaned_data.get('cpf')
        if cpf:
            cpf_sem_mascara = re.sub(r'\D', '', cpf)  
            return cpf_sem_mascara
        return cpf
