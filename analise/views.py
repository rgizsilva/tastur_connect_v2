# analise/views.py

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import AnaliseDados
from .serializers import AnaliseDadosSerializer

# -----------------------------------------------------------------------------
# API VIEWSET - APENAS LEITURA (GET)
# -----------------------------------------------------------------------------

class AnaliseDadosViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint que permite a visualização do último dado de análise.
    - Apenas operações de leitura (GET) são permitidas.
    - Requer que o usuário esteja autenticado para acessar.
    """
    serializer_class = AnaliseDadosSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Este método LÊ e retorna o registro mais recente que já existe.
        Ele não cria nem modifica nada.
        """
        latest_analysis = AnaliseDados.objects.order_by('-data_analise').first()
        if latest_analysis:
            # Retorna o registro encontrado dentro de uma lista
            return [latest_analysis]
        # Se não houver dados, retorna uma lista vazia
        return AnaliseDados.objects.none()

# -----------------------------------------------------------------------------
# VIEW TRADICIONAL (PÁGINA HTML) - Opcional
# -----------------------------------------------------------------------------
@login_required
def relatorio_analise(request):
    """
    Renderiza uma página HTML com o último relatório de análise.
    """
    try:
        dados_analise = AnaliseDados.objects.latest('data_analise')
    except AnaliseDados.DoesNotExist:
        dados_analise = None

    context = {'dados': dados_analise}
    return render(request, 'analise/relatorio_analise.html', context)
