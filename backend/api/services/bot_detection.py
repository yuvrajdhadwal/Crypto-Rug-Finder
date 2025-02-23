import numpy as np
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import StandardScaler
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from ..models import CryptoTokenSpam

# Common SPAM keywords
SPAM_KEYWORDS = {
    'airdrop', '100x', 'pump', 'moon', 'guaranteed', 'free crypto', 'investment',
    'daily profit', 'easy money', 'DOGE', "diamond", "hold", 
}

def extract_features(posts):
    analyzer = SentimentIntensityAnalyzer()
    vectorizer = TfidfVectorizer(max_features=500, stop_words="english")

    # compute tf-idf matrix

def compute_bot_activity(posts, comments):
    """Computes percentage of posts and comments are potentially bots/spam"""

    posts_text = [post.text for post in posts]
    comments_text = [comment.text for comment in comments]

    post_spam_labels = detect_spam(posts_text)
    comment_spam_labels = detect_spam(comments_text)

    post_spam_percentage = (sum(post_spam_labels) / len(posts)) * 100 if posts else 0
    comment_spam_percentage = (sum(comment_spam_labels) / len(posts)) * 100 if comments else 0

    CryptoTokenSpam.objects.create(
        crypto_token=posts[0].cryto_token,
        post_spam=post_spam_percentage,
        comment_spam=comment_spam_percentage
    )