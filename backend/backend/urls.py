# backend/api/urls.py
from django.urls import path, include
from api.views import market_data_view

urlpatterns = [
    path('api/', include('api.urls')),
]
