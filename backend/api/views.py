# backend/api/views.py
import os
import praw
from dotenv import load_dotenv

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .services.coingecko import fetch_market_data  # Your existing fetch function
from .services.honeypot import check_honeypot

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

    if not query:
        return Response({"error": "Crypto token required to query"}, status=status.HTTP_400_BAD_REQUEST)
    
    subreddit_list = [
        'cryptocurrency',
        'cryptomoonshots',
        'defi',
        'cryptoscams',
        'binance'
    ]

    results = []

    try:
        for subreddit_name in subreddit_list:
            subreddit = reddit.subreddit(subreddit_name)
            
            for post in subreddit.search(query=query, limit=limit):
                results.append({
                    "subreddit": subreddit_name,
                    "title": post.title,
                    "text": post.selftext,
                    "upvotes": post.score,
                    "comment_count": post.num_comments,
                    "comments": post.comments
                })
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    return Response({"posts": results[3]}, status=status.HTTP_200_OK)

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