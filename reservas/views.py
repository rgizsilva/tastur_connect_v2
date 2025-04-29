from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Reserva
from clientes.models import Cliente
from parceiros.models import Parceiro
from .forms import ReservaForm, ConsultaReservaForm

@login_required
def cadastrar_reserva(request):
    """Cadastro de novas reservas (apenas para colaboradores)"""
    if request.method == 'POST':
        form = ReservaForm(request.POST)
        if form.is_valid():
            reserva = form.save()
            # Atualizar o status de possui_reserva do cliente
            cliente = reserva.cpf_cliente
            cliente.possui_reserva = True
            cliente.save()
            messages.success(request, 'Reserva cadastrada com sucesso!')
            return redirect('reservas:consultar_reserva')
        else:
            messages.error(request, 'Erro ao cadastrar reserva. Verifique os dados informados.')
    else:
        form = ReservaForm()
    return render(request, 'reservas/cadastrar_reserva.html', {'form': form})

@login_required
def consultar_reserva(request):
    """Consulta de reservas (apenas para colaboradores)"""
    form = ConsultaReservaForm(request.GET or None)
    reservas = []
    
    if form.is_valid() and request.GET:
        numero_reserva = form.cleaned_data.get('numero_reserva')
        cpf_cliente = form.cleaned_data.get('cpf_cliente')
        
        if numero_reserva:
            reservas = Reserva.objects.filter(numero_reserva=numero_reserva)
        elif cpf_cliente:
            reservas = Reserva.objects.filter(cpf_cliente__cpf_cliente=cpf_cliente)
        else:
            reservas = Reserva.objects.all()
    
    return render(request, 'reservas/consultar_reserva.html', {
        'form': form,
        'reservas': reservas
    })

@login_required
def editar_reserva(request, numero):
    """Edição de reservas existentes (apenas para colaboradores)"""
    reserva = get_object_or_404(Reserva, numero_reserva=numero)
    
    if request.method == 'POST':
        form = ReservaForm(request.POST, instance=reserva)
        if form.is_valid():
            # Verificar se o cliente foi alterado
            cliente_antigo = reserva.cpf_cliente
            reserva_atualizada = form.save()
            
            # Se o cliente foi alterado, atualizar o status de possui_reserva
            if cliente_antigo != reserva_atualizada.cpf_cliente:
                # Verificar se o cliente antigo possui outras reservas
                outras_reservas_cliente_antigo = Reserva.objects.filter(cpf_cliente=cliente_antigo).exclude(numero_reserva=numero).exists()
                if not outras_reservas_cliente_antigo:
                    cliente_antigo.possui_reserva = False
                    cliente_antigo.save()
                
                # Atualizar o status do novo cliente
                novo_cliente = reserva_atualizada.cpf_cliente
                novo_cliente.possui_reserva = True
                novo_cliente.save()
            
            messages.success(request, 'Reserva atualizada com sucesso!')
            return redirect('reservas:consultar_reserva')
        else:
            messages.error(request, 'Erro ao atualizar reserva. Verifique os dados informados.')
    else:
        form = ReservaForm(instance=reserva)
    
    return render(request, 'reservas/editar_reserva.html', {'form': form, 'reserva': reserva})

@login_required
def excluir_reserva(request, numero):
    """Exclusão de reservas (apenas para colaboradores)"""
    reserva = get_object_or_404(Reserva, numero_reserva=numero)
    
    if request.method == 'POST':
        try:
            # Atualizar o status de possui_reserva do cliente
            cliente = reserva.cpf_cliente
            # Verificar se o cliente possui outras reservas
            outras_reservas = Reserva.objects.filter(cpf_cliente=cliente).exclude(numero_reserva=numero).exists()
            if not outras_reservas:
                cliente.possui_reserva = False
                cliente.save()
            
            reserva.delete()
            messages.success(request, 'Reserva excluída com sucesso!')
        except Exception as e:
            messages.error(request, f'Erro ao excluir reserva: {str(e)}')
        
        return redirect('reservas:consultar_reserva')
    
    return render(request, 'reservas/excluir_reserva.html', {'reserva': reserva})

def consultar_reserva_cliente(request):
    """Consulta de reservas para clientes (acesso sem login)"""
    form = ConsultaReservaForm(request.GET or None)
    reservas = []
    
    if 'cliente_cpf' in request.session:
        cpf_cliente = request.session['cliente_cpf']
        reservas = Reserva.objects.filter(cpf_cliente__cpf_cliente=cpf_cliente)
    elif form.is_valid() and request.GET:
        numero_reserva = form.cleaned_data.get('numero_reserva')
        cpf_cliente = form.cleaned_data.get('cpf_cliente')
        
        if numero_reserva:
            reservas = Reserva.objects.filter(numero_reserva=numero_reserva)
        elif cpf_cliente:
            reservas = Reserva.objects.filter(cpf_cliente__cpf_cliente=cpf_cliente)
    
    return render(request, 'reservas/consultar_reserva_cliente.html', {
        'form': form,
        'reservas': reservas
    })
