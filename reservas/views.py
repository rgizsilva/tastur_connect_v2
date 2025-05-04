# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Reserva
from clientes.models import Cliente
from parceiros.models import Parceiro
from .forms import ReservaForm, ConsultaReservaForm

# views.py
@login_required
def cadastrar_reserva(request):
    if request.method == 'POST':
        form = ReservaForm(request.POST)
        if form.is_valid():
            reserva = form.save(commit=False)

            # Buscar e associar o Cliente
            cpf = form.cleaned_data['cpf_cliente']
            try:
                cliente = Cliente.objects.get(cpf_cliente=cpf)
                reserva.cpf_cliente = cliente
                reserva.nome_cliente = cliente.nome_completo  # Atribuindo automaticamente o nome do cliente
            except Cliente.DoesNotExist:
                form.add_error('cpf_cliente', 'Cliente não encontrado.')
                return render(request, 'reservas/cadastrar_reserva.html', {'form': form})

            # Agora o campo 'cnpj' recebe a instância de Parceiro, e não a string
            parceiro = form.cleaned_data.get('cnpj')
            if parceiro:  # Caso tenha um parceiro válido
                reserva.cnpj = parceiro  # Atribui a instância de Parceiro diretamente

            # Definir o colaborador responsável
            reserva.colaborador_responsavel = request.user.username

            # Salvar a reserva
            reserva.save()

            # Redirecionar para a página de consulta de reservas
            return redirect('reservas:consultar_reserva')  # Altere para consultar_reserva

    else:
        form = ReservaForm()

    return render(request, 'reservas/cadastrar_reserva.html', {'form': form})




@login_required
def consultar_reserva(request):
    form = ConsultaReservaForm(request.GET or None)  
    reservas = Reserva.objects.all()  

    if form.is_valid():
        cpf_cliente = form.cleaned_data.get('cpf_cliente')  

        if cpf_cliente:
            reservas = reservas.filter(cpf_cliente__cpf_cliente=cpf_cliente)

    return render(request, 'reservas/consultar_reserva.html', {'form': form, 'reservas': reservas})

@login_required
def editar_reserva(request, numero_reserva):
    reserva = get_object_or_404(Reserva, numero_reserva=numero_reserva)
    
    if request.method == 'POST':
        form = ReservaForm(request.POST, instance=reserva)
        if form.is_valid():
            form.save()
            messages.success(request, "Reserva editada com sucesso!")
            return redirect('reservas:consultar_reserva')
    else:
        form = ReservaForm(instance=reserva)
    
    return render(request, 'reservas/cadastrar_reserva.html', {'form': form, 'reserva': reserva})

@login_required
def excluir_reserva(request, numero_reserva):
    reserva = get_object_or_404(Reserva, numero_reserva=numero_reserva)
    
    if request.method == 'POST':
        reserva.delete()
        messages.success(request, "Reserva excluída com sucesso!")
        return redirect('reservas:consultar_reserva')
    
    return render(request, 'reservas/excluir_reserva.html', {'reserva': reserva})
