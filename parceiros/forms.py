from django import forms
from .models import Parceiro

class ParceiroForm(forms.ModelForm):
    class Meta:
        model = Parceiro
        fields = '__all__'
        widgets = {
            'data_entrada': forms.DateInput(attrs={'type': 'date'}),
        }

class ConsultaParceiroForm(forms.Form):
    cnpj = forms.CharField(max_length=18, required=False, label='CNPJ')
