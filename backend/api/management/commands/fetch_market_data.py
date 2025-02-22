# backend/pnd_app/management/commands/fetch_market_data.py
import os
import requests
from django.core.management.base import BaseCommand
from django.utils import timezone
from api.models import MarketData  # Adjust import if your model is in a different location

COINGECKO_API_KEY = os.getenv("COINGECKO_API_KEY", "YOUR_API_KEY")
BASE_URL = "https://api.coingecko.com/api/v3/coins/markets"

class Command(BaseCommand):
    help = 'Fetch market data from CoinGecko and update MarketData model'

    def handle(self, *args, **options):
        token_ids = ["ethereum", "uniswap", "bitcoin"]  # Customize as needed
        headers = {"x-cg-pro-api-key": COINGECKO_API_KEY}
        params = {
            "vs_currency": "usd",
            "ids": ",".join(token_ids),
            "order": "market_cap_desc",
            "per_page": len(token_ids),
            "page": 1,
            "sparkline": "false"
        }

        response = requests.get(BASE_URL, headers=headers, params=params, verify=False)
        if response.status_code == 200:
            data = response.json()
            for token in data:
                market_data, created = MarketData.objects.update_or_create(
                    token_id=token["id"],
                    defaults={
                        "name": token["name"],
                        "current_price": token["current_price"],
                        "total_volume": token["total_volume"],
                        "market_cap": token["market_cap"],
                        "last_updated": timezone.now()
                    }
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f"Created data for {token['name']}"))
                else:
                    self.stdout.write(self.style.SUCCESS(f"Updated data for {token['name']}"))
        else:
            self.stderr.write(f"Error: {response.status_code} {response.text}")
