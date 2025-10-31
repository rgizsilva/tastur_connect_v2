from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import AnaliseDadosViewSet, relatorio_analise

# ADICIONE ESTA LINHA
app_name = 'analise'

router = DefaultRouter()
router.register(r'dados', AnaliseDadosViewSet)

urlpatterns = [
    path('relatorio/', relatorio_analise, name='relatorio'),
]

urlpatterns += router.urls
