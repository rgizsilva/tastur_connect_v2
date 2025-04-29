from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Cliente
from .forms import ClienteForm, ConsultaClienteForm

@login_required
def cadastrar_cliente(request):
    """Cadastro de novos clientes (apenas para colaboradores)"""
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            cliente = form.save()
            messages.success(request, 'Cliente cadastrado com sucesso!')
            return redirect('clientes:consultar_cliente')
        else:
            messages.error(request, 'Erro ao cadastrar cliente. Verifique os dados informados.')
    else:
        form = ClienteForm()
    return render(request, 'clientes/cadastrar_cliente.html', {'form': form})

@login_required
def consultar_cliente(request):
    """Consulta de clientes (apenas para colaboradores)"""
    form = ConsultaClienteForm(request.GET or None)
    clientes = []
    
    if form.is_valid() and request.GET:
        cpf = form.cleaned_data.get('cpf')
        if cpf:
            clientes = Cliente.objects.filter(cpf_cliente__icontains=cpf)
        else:
            clientes = Cliente.objects.all()
    
    return render(request, 'clientes/consultar_cliente.html', {
        'form': form,
        'clientes': clientes
    })

@login_required
def editar_cliente(request, cpf):
    """Edição de clientes existentes (apenas para colaboradores)"""
    cliente = get_object_or_404(Cliente, cpf_cliente=cpf)
    
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cliente atualizado com sucesso!')
            return redirect('clientes:consultar_cliente')
        else:
            messages.error(request, 'Erro ao atualizar cliente. Verifique os dados informados.')
    else:
        form = ClienteForm(instance=cliente)
    
    return render(request, 'clientes/editar_cliente.html', {'form': form, 'cliente': cliente})

@login_required
def excluir_cliente(request, cpf):
    """Exclusão de clientes (apenas para colaboradores)"""
    cliente = get_object_or_404(Cliente, cpf_cliente=cpf)
    
    if request.method == 'POST':
        # Verificar se o cliente possui reservas antes de excluir
        if hasattr(cliente, 'reservas') and cliente.reservas.exists():
            messages.error(request, 'Não é possível excluir este cliente pois ele possui reservas associadas.')
            return redirect('clientes:consultar_cliente')
        
        try:
            cliente.delete()
            messages.success(request, 'Cliente excluído com sucesso!')
        except Exception as e:
            messages.error(request, f'Erro ao excluir cliente: {str(e)}')
        
        return redirect('clientes:consultar_cliente')
    
    return render(request, 'clientes/excluir_cliente.html', {'cliente': cliente})
