from django.urls import path
from .views import get_reddit_posts, get_stored_reddit_posts, market_data_view, on_chain_info
from .views import get_sentiment, honeypot_view, bot_activity_view

urlpatterns = [
    path("reddit/", get_reddit_posts, name="get_reddit_posts"),
    path("reddit_stored/", get_stored_reddit_posts, name="get_stored_reddit_posts"),
    path('market-data/', market_data_view, name='market-data'),
    path('token-price/', on_chain_info, name='token-price'),
    path('get_sentiment/', get_sentiment, name="get_sentiment"),
    path('honeypot/', honeypot_view, name='honeypot_view'),
    path('bot_check/', bot_activity_view, name='bot_check'),
]