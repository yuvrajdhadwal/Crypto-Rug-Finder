# backend/api/models.py
from django.db import models

class MarketData(models.Model):
    token_id = models.CharField(max_length=100, unique=True)  # e.g., "ethereum"
    name = models.CharField(max_length=100)                   # e.g., "Ethereum"
    current_price = models.FloatField()
    total_volume = models.FloatField()
    market_cap = models.FloatField()
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.token_id})"
