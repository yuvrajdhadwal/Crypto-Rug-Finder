from django.urls import path
from .views import get_reddit_posts, get_stored_reddit_posts

urlpatterns = [
    path("reddit/", get_reddit_posts, name="get_reddit_posts"),
    path("reddit/stored/", get_stored_reddit_posts, name="get_stored_reddit_posts"),

]
