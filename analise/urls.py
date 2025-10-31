# analise/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AnaliseDadosViewSet, relatorio_analise

app_name = 'analise'

# O Router cria as URLs da API automaticamente
router = DefaultRouter()
router.register(r'dados', AnaliseDadosViewSet, basename='analisedados')

urlpatterns = [
    # URL para a página HTML estática (opcional)
    path('relatorio/', relatorio_analise, name='relatorio'),
    
    # Inclui as URLs geradas pelo router:
    # - GET /api/analise/dados/
    # - POST /api/analise/dados/atualizar/
    path('', include(router.urls)),
]
