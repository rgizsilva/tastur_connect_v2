from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AnaliseDadosViewSet, relatorio_analise

app_name = 'analise'

router = DefaultRouter()
# MODIFIQUE ESTA LINHA PARA ADICIONAR O 'basename'
router.register(r'dados', AnaliseDadosViewSet, basename='analisedados')

urlpatterns = [
    path('relatorio/', relatorio_analise, name='relatorio'),
    path('', include(router.urls)),
]

urlpatterns += router.urls
