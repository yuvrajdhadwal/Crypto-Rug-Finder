from django.urls import path
from .views import get_reddit_posts, get_stored_reddit_posts, market_data_view, on_chain_info
from .views import get_sentiment, honeypot_view, bot_activity_view, rugpull_prediction
from .views import on_chain_info

urlpatterns = [
    path("reddit/", get_reddit_posts, name="get_reddit_posts"),
    path("reddit_stored/", get_stored_reddit_posts, name="get_stored_reddit_posts"),
    path('market-data/', market_data_view, name='market-data'),
    path('token-price/', on_chain_info, name='token-price'),
    path('get_sentiment/', get_sentiment, name="get_sentiment"),
    path('honeypot/', honeypot_view, name='honeypot_view'),
    path('bot_check/', bot_activity_view, name='bot_check'),
    path('predict-rugpull/', rugpull_prediction, name='rugpull_prediction'),
    path('on_chain_info', on_chain_info, name="on_chain_info")
]
