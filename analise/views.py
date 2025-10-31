from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import AnaliseDados
from .serializers import AnaliseDadosSerializer
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

class AnaliseDadosViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint que permite que os dados de análise sejam visualizados.
    Apenas leitura e requer autenticação.
    """
    queryset = AnaliseDados.objects.all().order_by('-data_analise')
    serializer_class = AnaliseDadosSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Como o modelo foi projetado para ter apenas um registro (o mais recente),
        # podemos retornar o último registro.
        return AnaliseDados.objects.all().order_by('-data_analise')[:1]

@login_required
def relatorio_analise(request):
    """
    View para a página de visualização do relatório de análise de dados.
    """
    try:
        dados_analise = AnaliseDados.objects.latest('data_analise')
    except AnaliseDados.DoesNotExist:
        dados_analise = None

    context = {
        'dados': dados_analise
    }
    return render(request, 'analise/relatorio_analise.html', context)
