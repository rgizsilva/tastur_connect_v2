# analise/views.py

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets, status, mixins # <--- IMPORTAR MIXINS
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
import random

from .models import AnaliseDados
from .serializers import AnaliseDadosSerializer

# -----------------------------------------------------------------------------
# API VIEWSET - VERSÃO CORRIGIDA PARA MOSTRAR A AÇÃO POST
# -----------------------------------------------------------------------------

# MUDANÇA PRINCIPAL: Em vez de ReadOnlyModelViewSet, vamos compor o nosso.
class AnaliseDadosViewSet(mixins.ListModelMixin, # Adiciona a funcionalidade de listar (GET /dados/)
                          viewsets.GenericViewSet): # A base para ViewSets customizados
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
        Cria um novo registro de AnaliseDados com dados e data atuais.
        """
        try:
            novo_registro = AnaliseDados.objects.create(
                pacotes_vendidos=random.randint(50, 250),
                idade_media_clientes=random.uniform(25.0, 55.0),
                valor_medio_pacotes=random.uniform(1500.0, 4500.0),
                valor_minimo_pacote=random.uniform(700.0, 1200.0),
                valor_maximo_pacote=random.uniform(5000.0, 10000.0)
            )
            serializer = self.get_serializer(novo_registro)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(
                {"error": f"Falha ao gerar nova análise: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

# -----------------------------------------------------------------------------
# VIEW TRADICIONAL (PÁGINA HTML) - Opcional
# -----------------------------------------------------------------------------
@login_required
def relatorio_analise(request):
    # ... (esta view não precisa de alterações)
    try:
        dados_analise = AnaliseDados.objects.latest('data_analise')
    except AnaliseDados.DoesNotExist:
        dados_analise = None
    context = {'dados': dados_analise}
    return render(request, 'analise/relatorio_analise.html', context)
