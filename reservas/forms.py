from django import forms
from .models import Reserva
from clientes.models import Cliente
from parceiros.models import Parceiro

class ReservaForm(forms.ModelForm):
    cpf_cliente = forms.CharField(
        label="CPF do Cliente",
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    
    cnpj = forms.CharField(
        max_length=14, 
        required=False, 
        widget=forms.TextInput(attrs={'class': 'form-control'}), 
        label="CNPJ do Parceiro"
    )

    class Meta:
        model = Reserva
        exclude = (
            'numero_reserva', 
            'data_entrada', 
            'nome_cliente', 
            'nome_fantasia', 
            'colaborador_responsavel',
            'cpf_cliente',
        )
        widgets = {
            'data_ida': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}), 
            'data_volta': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}), 
            'comentarios_adicionais': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cpf_cliente'].label = "CPF do Cliente"
        self.fields['cpf_cliente'].required = True 

        self.fields['cnpj'].label = "CNPJ do Parceiro"
        self.fields['cnpj'].required = True 

    def clean_cnpj(self):
        cnpj = self.cleaned_data.get('cnpj')
        if cnpj:
            try:
                parceiro = Parceiro.objects.get(cnpj=cnpj)
            except Parceiro.DoesNotExist:
                raise forms.ValidationError('Parceiro não encontrado.')
            return parceiro  
        return None
    
    
    def clean_cpf_cliente(self):
        cpf = self.cleaned_data.get('cpf_cliente')
        if cpf:
            if not Cliente.objects.filter(cpf_cliente=cpf).exists():
                raise forms.ValidationError('Cliente não encontrado com esse CPF.')
        return cpf




class ConsultaReservaForm(forms.Form):
    numero_reserva = forms.CharField(max_length=10, required=False, label='Número da Reserva')
    cpf_cliente = forms.CharField(max_length=14, required=False, label='CPF do Cliente')
