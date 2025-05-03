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
            try:
                # Pega as instâncias selecionadas 
                cliente_instance = form.cleaned_data['cpf_cliente']
                parceiro_instance = form.cleaned_data.get('cnpj') 

                reserva = form.save(commit=False)

               
                reserva.cpf_cliente = cliente_instance
                reserva.nome_cliente = cliente_instance.nome_completo

                
                if parceiro_instance:
                    reserva.cnpj = parceiro_instance
                    reserva.nome_fantasia = parceiro_instance.nome_fantasia
                else:
                    reserva.cnpj = None 
                    reserva.nome_fantasia = "" 

                
                if request.user.is_authenticated:
                    reserva.colaborador_responsavel = request.user.get_full_name() or request.user.username
                else:
                    messages.error(request, "Erro crítico: Usuário não autenticado.")
                    return render(request, 'reservas/cadastrar_reserva.html', {'form': form})

                reserva.save()

                
                cliente_instance.possui_reserva = True
                cliente_instance.save()

                messages.success(request, 'Reserva cadastrada com sucesso!')
                return redirect('reservas:consultar_reserva')
            
            except Exception as e:
                 messages.error(request, f'Ocorreu um erro inesperado ao salvar a reserva: {e}')
                 print(f"Erro ao salvar reserva: {e}") 
        else:
            error_list = "; ".join([f"{field}: {error[0]}" for field, error in form.errors.items()])
            messages.error(request, f'Erro ao cadastrar reserva. Verifique os dados: {error_list}')
            print(f"Erro no formulário de reserva: {form.errors}")
    else: 
        form = ReservaForm()

    return render(request, 'reservas/cadastrar_reserva.html', {'form': form})

@login_required
def consultar_reserva(request):
    form = ConsultaReservaForm(request.GET or None)
    reservas = Reserva.objects.all()  

    if form.is_valid():
        numero_reserva = form.cleaned_data.get('numero_reserva')
        cpf_cliente = form.cleaned_data.get('cpf_cliente')

        if numero_reserva:
            reservas = reservas.filter(numero_reserva=numero_reserva)
        if cpf_cliente:
            reservas = reservas.filter(cpf_cliente__cpf=cpf_cliente)

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
