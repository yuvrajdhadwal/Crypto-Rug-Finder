# backend/api/urls.py
from django.urls import path
from api.views import market_data_view

urlpatterns = [
    path('market-data/', market_data_view, name='market-data'),
]
