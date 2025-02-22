import requests
import os
from dotenv import load_dotenv
import pandas as pd
import tweepy
import tweepy.client

def request_tweets(token_ids):
    """
    Fetch relevant tweets

    :param token_ids: List of token IDs (e.g., ["ethereum", "uniswap", "bitcoin"])
    :return: List of market data dictionaries
    """

    load_dotenv()

    # consumer_key = os.getenv('CONSUMER_KEY')
    # consumer_secret = os.getenv('CONSUMER_SECRET')
    # access_token = os.getenv('ACCESS_TOKEN')
    # access_token_secret = os.getenv('ACCESS_TOKEN_SECRET')
    bearer_token = os.getenv('BEARER_TOKEN')

    # auth = tweepy.OAuth1UserHandler(
    #     consumer_key, consumer_secret,
    #     access_token, access_token_secret
    # )
    
    client = tweepy.Client(bearer_token)

    # tweepy_api = tweepy.API(auth, wait_on_rate_limit=True)

    token_name = '$' + token_ids
    token_coin = token_ids + ' coin'

    search_query = "%s OR %s -is:retweet lang:en"
    tweet_fields=["id", "text", "author_id", "created_at", "public_metrics"]
    tweets = client.search_recent_tweets(query=search_query, max_results=100, tweet_fields=tweet_fields)

