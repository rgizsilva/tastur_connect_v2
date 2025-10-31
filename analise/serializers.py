from rest_framework import serializers
from .models import AnaliseDados

class AnaliseDadosSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnaliseDados
        fields = '__all__'
