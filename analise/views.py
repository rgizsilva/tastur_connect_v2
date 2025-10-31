# analise/views.py

# Imports do Django e do Django REST Framework
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
import random # Usaremos para simular a nova análise

# Imports locais do seu app 'analise'
from .models import AnaliseDados
from .serializers import AnaliseDadosSerializer

# -----------------------------------------------------------------------------
# API VIEWSET
# Esta classe cria os endpoints da API
# -----------------------------------------------------------------------------

class AnaliseDadosViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint para visualizar e ATUALIZAR os dados de análise.
    - GET /api/analise/dados/ -> Retorna a análise mais recente.
    - POST /api/analise/dados/atualizar/ -> Gera um novo registro de análise.
    """
    serializer_class = AnaliseDadosSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Este método é para a requisição GET.
        Ele apenas LÊ e retorna o registro mais recente que já existe.
        """
        latest_analysis = AnaliseDados.objects.order_by('-data_analise').first()
        if latest_analysis:
            return [latest_analysis]
        return AnaliseDados.objects.none()

    @action(detail=False, methods=['post'])
    def atualizar(self, request):
        """
        Esta é a nova ação que CRIA um novo registro de análise.
        É acionada por uma requisição POST para .../dados/atualizar/.
        """
        try:
            # No futuro, você pode substituir os dados aleatórios por cálculos reais
            # baseados em suas outras tabelas (Clientes, Reservas, etc.).
            novo_registro = AnaliseDados.objects.create(
                pacotes_vendidos=random.randint(50, 250),
                idade_media_clientes=random.uniform(25.0, 55.0),
                valor_medio_pacotes=random.uniform(1500.0, 4500.0),
                valor_minimo_pacote=random.uniform(700.0, 1200.0),
                valor_maximo_pacote=random.uniform(5000.0, 10000.0)
            )

            # O campo 'data_analise' com 'auto_now_add=True' no modelo
            # garantirá que a data e hora exatas da criação sejam salvas.

            # Serializa o novo registro para retorná-lo na resposta da API
            serializer = self.get_serializer(novo_registro)
            
            # Retorna o novo dado criado com um status 201 (Created)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            # Em caso de erro durante a criação, retorna uma mensagem clara
            return Response(
                {"error": f"Falha ao gerar nova análise: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

# -----------------------------------------------------------------------------
# VIEW TRADICIONAL (PÁGINA HTML) - Opcional
# Esta view não é mais necessária para o fluxo da API, mas pode ser mantida
# se você tiver um link direto para uma página de relatório estático.
# -----------------------------------------------------------------------------

@login_required
def relatorio_analise(request):
    """
    Renderiza uma página HTML com o último relatório de análise (não é usado pelo botão da API).
    """
    try:
        dados_analise = AnaliseDados.objects.latest('data_analise')
    except AnaliseDados.DoesNotExist:
        dados_analise = None

    context = {'dados': dados_analise}
    return render(request, 'analise/relatorio_analise.html', context)
