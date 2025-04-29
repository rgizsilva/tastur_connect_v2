from django.urls import path
from . import views

app_name = 'parceiros'

urlpatterns = [
    path('cadastrar/', views.cadastrar_parceiro, name='cadastrar_parceiro'),
    path('consultar/', views.consultar_parceiro, name='consultar_parceiro'),
    path('editar/<str:cnpj>/', views.editar_parceiro, name='editar_parceiro'),
    path('excluir/<str:cnpj>/', views.excluir_parceiro, name='excluir_parceiro'),
]
