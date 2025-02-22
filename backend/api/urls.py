from django.urls import path
from .views import get_reddit_posts, get_stored_reddit_posts, market_data_view

urlpatterns = [
    path("reddit/", get_reddit_posts, name="get_reddit_posts"),
    path("reddit/stored/", get_stored_reddit_posts, name="get_stored_reddit_posts"),
    path('market-data/', market_data_view, name='market-data'),
]
