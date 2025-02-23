# backend/api/models.py
from django.db import models

class MarketData(models.Model):
    token_id = models.CharField(max_length=100, unique=True)  # e.g., "ethereum"
    name = models.CharField(max_length=100)                   # e.g., "Ethereum"
    current_price = models.FloatField()
    total_volume = models.FloatField()
    market_cap = models.FloatField()
    last_updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.token_id})"
    

class RedditPost(models.Model):
    crypto_token = models.CharField(max_length=100)
    subreddit = models.CharField(max_length=100)
    title = models.TextField()
    text = models.TextField(blank=True, null=True)
    post_author = models.CharField(max_length=100, null=True, blank=True)
    upvotes = models.IntegerField()
    comments_count = models.IntegerField()
    url = models.URLField(unique=True)  # Ensure uniqueness to avoid duplicates
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp for tracking

    def __str__(self):
        return self.title

class RedditComment(models.Model):
    post = models.ForeignKey(RedditPost, related_name="comments", on_delete=models.CASCADE)
    author = models.CharField(max_length=100)
    text = models.TextField()
    upvotes = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp for tracking

    def __str__(self):
        return f"Comment by {self.author} on {self.post.title}"
    

class CryptoTokenSentiment(models.Model):
    crypto_token = models.CharField(max_length=100)
    overall_title_sentiment_value = models.FloatField()
    overall_text_sentiment_value = models.FloatField()
    overall_comment_sentiment_value = models.FloatField()
    overall_sentiment_value = models.FloatField()
    overall_title_sentiment = models.CharField(max_length=100)
    overall_text_sentiment = models.CharField(max_length=100)
    overall_comment_sentiment = models.CharField(max_length=100)
    overall_sentiment = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)


class CryptoTokenSpam(models.Model):
    crypto_token = models.CharField(max_length=100)
    post_spam = models.FloatField() # percentage of content that is spam
    comment_spam = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)