from django import forms
from .models import Cliente
import re

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = '__all__'
        widgets = {
            'data_nascimento': forms.DateInput(attrs={'type': 'date'}), 
        }

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
