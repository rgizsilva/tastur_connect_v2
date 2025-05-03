from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import ColaboradorLoginForm, ClienteLoginForm, ColaboradorForm
from .models import Colaborador
from clientes.models import Cliente

def home(request):
    """Página inicial do sistema Tastur Connect"""
    return render(request, 'core/home.html')

def login_colaborador(request):
    """Página de login para colaboradores"""
    if request.method == 'POST':
        form = ColaboradorLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Bem-vindo, {user.first_name or username}!')
                return redirect('core:selecao_colaborador')
            else:
                messages.error(request, 'Usuário ou senha inválidos')
        else:
            messages.error(request, 'Erro no formulário')
    else:
        form = ColaboradorLoginForm()
    return render(request, 'core/login_colaborador.html', {'form': form})

def login_cliente(request):
    """Página de login para clientes"""
    if request.method == 'POST':
        form = ClienteLoginForm(request.POST)
        if form.is_valid():
            cpf = form.cleaned_data.get('cpf')
            try:
                cliente = Cliente.objects.get(cpf_cliente=cpf)
                request.session['cliente_cpf'] = cpf
                request.session['cliente_nome'] = cliente.nome_completo
                messages.success(request, f'Bem-vindo, {cliente.nome_completo}!')
                return redirect('core:selecao_cliente')
            except Cliente.DoesNotExist:
                messages.error(request, 'CPF não encontrado')
        else:
            messages.error(request, 'Erro no formulário')
    else:
        form = ClienteLoginForm()
    return render(request, 'core/login_cliente.html', {'form': form})

def logout_view(request):
    """Função para realizar logout"""
    if request.user.is_authenticated:
        username = request.user.username
        logout(request)
        messages.success(request, f'Usuário {username} desconectado com sucesso!')
    elif 'cliente_cpf' in request.session:
        cliente_nome = request.session.get('cliente_nome', 'Cliente')
        del request.session['cliente_cpf']
        if 'cliente_nome' in request.session:
            del request.session['cliente_nome']
        messages.success(request, f'{cliente_nome} desconectado com sucesso!')
    return redirect('core:home')

@login_required
def selecao_colaborador(request):
    """Página de seleção de opções para colaboradores"""
    return render(request, 'core/selecao_colaborador.html')

def selecao_cliente(request):
    """Página de seleção de opções para clientes"""
    if 'cliente_cpf' not in request.session:
        messages.error(request, 'Você precisa fazer login para acessar esta página')
        return redirect('core:login_cliente')
    return render(request, 'core/selecao_cliente.html')

@login_required
def cadastrar_colaborador(request):
    """Cadastro de novos colaboradores (apenas para administradores)"""
    if not request.user.is_superuser:
        messages.error(request, 'Você não tem permissão para acessar esta página')
        return redirect('core:selecao_colaborador')
        
    if request.method == 'POST':
        form = ColaboradorForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            # Criar usuário
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )
            
            # Criar colaborador associado ao usuário
            colaborador = Colaborador(
                user=user,
                nome_completo=form.cleaned_data['nome_completo'],
                telefone=form.cleaned_data['telefone']
            )
            colaborador.save()
            
            messages.success(request, 'Colaborador cadastrado com sucesso!')
            return redirect('core:selecao_colaborador')
    else:
        form = ColaboradorForm()
    
    return render(request, 'core/cadastrar_colaborador.html', {'form': form})
