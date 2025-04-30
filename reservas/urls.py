
from django.urls import path
from . import views

app_name = 'reservas'

urlpatterns = [
    path('consultar/', views.consultar_reserva, name='consultar_reserva'),  # Rota para consultar reservas
    path('cadastrar/', views.cadastrar_reserva, name='cadastrar_reserva'),  # Rota para cadastrar reserva
    path('editar/<str:numero_reserva>/', views.editar_reserva, name='editar_reserva'),  # Rota para editar reserva
    path('excluir/<str:numero_reserva>/', views.excluir_reserva, name='excluir_reserva'),  # Rota para excluir reserva
]
