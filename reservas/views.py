# reservas/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Reserva
from clientes.models import Cliente
from parceiros.models import Parceiro
from core.models import Colaborador # Importar Colaborador
from .forms import ReservaForm, ConsultaReservaForm

@login_required
def cadastrar_reserva(request):
    """Cadastro de novas reservas (apenas para colaboradores)"""
    if request.method == 'POST':
        form = ReservaForm(request.POST)
        if form.is_valid():
            try:
                # Pega as instâncias de Cliente e Parceiro selecionadas no form
                cliente_instance = form.cleaned_data['cpf_cliente']
                parceiro_instance = form.cleaned_data['cnpj']

                # Cria a instância da Reserva sem salvar no banco ainda
                reserva = form.save(commit=False)

                # Atribui as instâncias corretas e preenche os nomes
                reserva.cpf_cliente = cliente_instance
                reserva.nome_cliente = cliente_instance.nome_completo
                reserva.cnpj = parceiro_instance
                reserva.nome_fantasia = parceiro_instance.nome_fantasia

                # Preenche o colaborador responsável (usuário logado)
                try:
                    # Tenta pegar o nome completo do perfil Colaborador
                    reserva.colaborador_responsavel = request.user.colaborador.nome_completo
                except (AttributeError, Colaborador.DoesNotExist):
                    # Se não encontrar, usa o nome do usuário ou username
                    reserva.colaborador_responsavel = request.user.get_full_name() or request.user.username

                # Agora salva a reserva completa no banco
                reserva.save()

                # Atualiza o status do cliente
                cliente_instance.possui_reserva = True
                cliente_instance.save()

                messages.success(request, 'Reserva cadastrada com sucesso!')
                return redirect('reservas:consultar_reserva')
            except Exception as e:
                 # Captura qualquer erro inesperado durante o processo
                 messages.error(request, f'Ocorreu um erro inesperado: {e}')
                 print(f"Erro ao salvar reserva: {e}") # Log do erro para debug
        else:
            # Se o formulário for inválido, mostra os erros
            error_list = "; ".join([f"{field}: {error[0]}" for field, error in form.errors.items()])
            messages.error(request, f'Erro ao cadastrar reserva. Verifique os dados: {error_list}')
            print(form.errors) # Log dos erros do formulário para debug
    else:
        form = ReservaForm()

    # Preenche o campo oculto do colaborador com o nome do usuário logado para o template inicial
    try:
        initial_colaborador = request.user.colaborador.nome_completo
    except (AttributeError, Colaborador.DoesNotExist):
        initial_colaborador = request.user.get_full_name() or request.user.username
    form.fields['colaborador_responsavel'].initial = initial_colaborador

    return render(request, 'reservas/cadastrar_reserva.html', {'form': form})



