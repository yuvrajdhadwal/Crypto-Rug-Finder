from ..models import RedditComment, RedditPost, CryptoTokenSentiment
from ..views import get_reddit_posts
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

def create_sentiment(token):
    '''creates sentiment of a certain crypto token'''
    
    posts = RedditPost.objects.filter(crypto_token=token).order_by("-created_at")

    if not posts.exists():        
        request = type('Request', (object,), {"GET": {"query": token, "limit": 15, "max_comments": 5}})
        response = get_reddit_posts(request)
        
        if response.status_code != 200 or not response.data.get("posts"):
            return None  # No posts found even after fetching

        # Re-fetch posts after updating
        posts = RedditPost.objects.filter(crypto_token=token).order_by("-created_at")

        if not posts.exists():
            return None  # Still no data, return failure
    
    analyzer = SentimentIntensityAnalyzer()

    title_sentiments = []
    text_sentiments = []
    comment_sentiments = []

    for post in posts:
        post_comments = RedditComment.objects.filter(post=post)

        title_sentiment = analyzer.polarity_scores(post.title)["compound"]
        text_sentiment = analyzer.polarity_scores(post.text)['compound']

        comment_sentiment_list = [analyzer.polarity_scores(comment.text)['compound'] for comment in post_comments]
        avg_comment_sentiment = sum(comment_sentiment_list) / len(comment_sentiment_list) if comment_sentiment_list else 0

        title_sentiments.append(title_sentiment)
        text_sentiments.append(text_sentiment)
        comment_sentiments.append(avg_comment_sentiment)

    overall_title_sentiment = sum(title_sentiments) / len(title_sentiments) if title_sentiments else 0
    overall_text_sentiment = sum(text_sentiments) / len(text_sentiments) if text_sentiments else 0
    overall_comment_sentiment = sum(comment_sentiments) / len(comment_sentiments) if comment_sentiments else 0

    overall_sentiment = (overall_title_sentiment * 0.3) + (overall_text_sentiment * 0.4) + (overall_comment_sentiment * 0.3)

    sentiment, created = CryptoTokenSentiment.objects.get_or_create(
            crypto_token=token,
            defaults={
                "crypto_token": token,
                "overall_title_sentiment": overall_title_sentiment,
                "overall_text_sentiment": overall_text_sentiment,
                "overall_comment_sentiment": overall_comment_sentiment,
                "overall_sentiment": overall_sentiment,
            }
        )
    
    return "it worked"
