# backend/api/views.py
import os
import praw
from dotenv import load_dotenv

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .services.coingecko import fetch_market_data  # Your existing fetch function
from .services.honeypot import check_honeypot

from .models import RedditComment, RedditPost

load_dotenv()

reddit = praw.Reddit(
    client_id= os.getenv('CLIENT_ID'),
    client_secret= os.getenv('CLIENT_SECRET'),
    username= os.getenv('REDDIT_USERNAME'),
    password= os.getenv('REDDIT_PASSWORD'),
    user_agent= os.getenv('REDDIT_APP')   
)


@api_view(['GET'])
def market_data_view(request):
    """
    Example: /market-data/?tokens=ethereum,uniswap,bitcoin
    """
    # Read the 'tokens' query param; default to 'ethereum,bitcoin' if none provided
    tokens_str = request.GET.get('tokens', 'ethereum,bitcoin')
    # Split on commas to get a list
    tokens_list = tokens_str.split(',')
    
    # Now fetch data from CoinGecko for these tokens
    data = fetch_market_data(tokens_list)

    return Response(data)

@api_view(['GET'])
def get_reddit_posts(request):
    """
    API endpoint to fetch Reddit posts based on a query.
    Example request: /api/reddit/?query=Bitcoin&limit=5
    """

    query = request.GET.get("query", None)
    limit = int(request.GET.get("limit", 10)) # I defaulted it to 10 for now
    max_comments = int(request.GET.get("max_comments", 10))

    if not query:
        return Response({"error": "Crypto token required to query"}, status=status.HTTP_400_BAD_REQUEST)
    
    subreddit_list = [
        'cryptocurrency',
        'cryptomoonshots',
        'cryptoscams',
    ]

    reddit_query = f"${query.lower()} OR {query.lower()} token OR {query.lower()} coin"

    results = []

    try:
        for subreddit_name in subreddit_list:
            subreddit = reddit.subreddit(subreddit_name)
            
            for post in subreddit.search(query=reddit_query, limit=limit):

                post_author = post.author.name if post.author else "Unknown"

                # Create post object
                reddit_post, created = RedditPost.objects.get_or_create(
                    url=post.url,
                    defaults={
                        "subreddit": subreddit_name,
                        "crypto_token": query,
                        "title": post.title,
                        "text": post.selftext,
                        "upvotes": post.score,
                        "comments_count": post.num_comments,
                        "url": post.url,
                        "post_author": post_author,
                    }
                )

                # Fetch and store comments
                if created:
                    post.comments.replace_more(limit=0)  # Remove "More Comments" button
                    for comment in post.comments[:max_comments]:
                        RedditComment.objects.create(
                            post=reddit_post,
                            author=comment.author.name if comment.author else "Unknown",
                            text=comment.body,
                            upvotes=comment.score
                        )

                # Append to response
                results.append({
                    "subreddit": subreddit_name,
                    "crypto_token": query,
                    "title": post.title,
                    "text": post.selftext,
                    "post_author": post_author,
                    "upvotes": post.score,
                    "comments_count": post.num_comments,
                    "url": post.url,
                    "comments": [{"author": c.author, "text": c.text, "upvotes": c.upvotes}
                                 for c in reddit_post.comments.all()[:max_comments]]
                })

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    return Response({"posts": results[:3]}, status=status.HTTP_200_OK) # returns the top 3 posts

@api_view(["GET"])
def get_stored_reddit_posts(request):
    """
    Retrieve stored Reddit posts filtered by token (query).
    Example request: /api/reddit/stored/?query=Bitcoin
    """
    token = request.GET.get("query", None)

    if not token:
        return Response({"error": "Query parameter is required."}, status=status.HTTP_400_BAD_REQUEST)

    posts = RedditPost.objects.filter(crypto_token=token).order_by("-created_at")

    if not posts.exists():
        return Response({"error": "No data found for this query."}, status=status.HTTP_404_NOT_FOUND)

    results = list(posts.values(
    "crypto_token", "subreddit", "title", "text", "post_author",
    "upvotes", "comments_count", "url"
    ))

    return Response({"posts": results}, status=status.HTTP_200_OK)

@api_view(['GET'])
def honeypot_view(request):
    """
    Example: GET /api/honeypot/?token=0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48&chain=eth
    """
    token = request.GET.get("token", "")
    chain = request.GET.get("chain", "eth")
    
    if not token:
        return Response({"error": "Missing 'token' parameter"}, status=400)
    
    data = check_honeypot(token, chain)
    return Response(data)
