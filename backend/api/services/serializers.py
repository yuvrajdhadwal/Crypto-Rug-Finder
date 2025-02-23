# backend/api/serializers.py
from rest_framework import serializers
from api.models import MarketData

class MarketDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarketData
        fields = '__all__'
