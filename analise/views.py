# Imports do Django e do Django REST Framework
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

# Imports locais do seu app 'analise'
from .models import AnaliseDados
from .serializers import AnaliseDadosSerializer

# -----------------------------------------------------------------------------
# API VIEWSET
# Esta classe cria o endpoint da API em /api/analise/dados/
# -----------------------------------------------------------------------------

class AnaliseDadosViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint que permite a visualização dos dados de análise.

    - Apenas operações de leitura (GET) são permitidas.
    - Requer que o usuário esteja autenticado para acessar.
    - Por padrão, retorna apenas o registro de análise mais recente.
    """
    serializer_class = AnaliseDadosSerializer
    permission_classes = [IsAuthenticated]  # Protege o endpoint, exigindo login

    def get_queryset(self):
        """
        Sobrescreve o método padrão para garantir que a API sempre retorne
        apenas o registro de análise mais recente em uma lista.
        
        Isso é mais eficiente do que buscar todos os registros do banco de dados.
        """
        # Busca o objeto mais recente pela data de análise
        latest_analysis = AnaliseDados.objects.order_by('-data_analise').first()
        
        # Se um registro for encontrado, retorna-o dentro de uma lista (como esperado pelo ViewSet).
        if latest_analysis:
            return [latest_analysis]
            
        # Se a tabela estiver vazia, retorna um queryset vazio para evitar erros.
        return AnaliseDados.objects.none()

# -----------------------------------------------------------------------------
# VIEW TRADICIONAL (PÁGINA HTML)
# Esta função gera a página HTML em /api/analise/relatorio/
# -----------------------------------------------------------------------------

@login_required  # Garante que apenas usuários logados possam ver a página
def relatorio_analise(request):
    """
    Renderiza a página HTML com o relatório de análise de dados.
    
    Busca o registro mais recente da análise no banco de dados e o envia
    para o template 'analise/relatorio_analise.html'.
    """
    dados_analise = None  # Inicializa a variável como None
    try:
        # Busca o objeto mais recente usando o método 'latest()', que é otimizado para isso.
        dados_analise = AnaliseDados.objects.latest('data_analise')
    except AnaliseDados.DoesNotExist:
        # Se a tabela estiver vazia, 'dados_analise' permanecerá None.
        # O template já está preparado para lidar com essa situação.
        pass

    # Prepara o contexto para enviar os dados para o template
    context = {
        'dados': dados_analise
    }
    
    # Renderiza o template HTML com os dados
    return render(request, 'analise/relatorio_analise.html', context)
