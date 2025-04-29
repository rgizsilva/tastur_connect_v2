from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from .models import Colaborador

class ColaboradorLoginForm(AuthenticationForm):
    username = forms.CharField(label='E-mail ou CPF', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Senha', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class ClienteLoginForm(forms.Form):
    cpf = forms.CharField(label='CPF', max_length=14, widget=forms.TextInput(attrs={'class': 'form-control'}))
    senha = forms.CharField(label='Senha', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class ColaboradorForm(forms.Form):
    nome_completo = forms.CharField(max_length=100)
    username = forms.CharField(max_length=150)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    telefone = forms.CharField(max_length=15)
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError('As senhas não coincidem')
        
        return cleaned_data
