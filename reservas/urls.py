from django.urls import path
from . import views

app_name = 'reservas'

urlpatterns = [
    path('cadastrar/', views.cadastrar_reserva, name='cadastrar_reserva'),
    path('consultar/', views.consultar_reserva, name='consultar_reserva'),
    path('consultar/cliente/', views.consultar_reserva_cliente, name='consultar_reserva_cliente'),
    path('editar/<str:numero>/', views.editar_reserva, name='editar_reserva'),
    path('excluir/<str:numero>/', views.excluir_reserva, name='excluir_reserva'),
]
