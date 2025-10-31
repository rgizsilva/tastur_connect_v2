from rest_framework import serializers
from .models import AnaliseDados

class AnaliseDadosSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnaliseDados
        # Os campos correspondem exatamente ao seu modelo
        fields = [
            'id', 
            'data_analise', 
            'pacotes_vendidos', 
            'idade_media_clientes', 
            'valor_medio_pacotes',
            'valor_minimo_pacote',
            'valor_maximo_pacote'
        ]
