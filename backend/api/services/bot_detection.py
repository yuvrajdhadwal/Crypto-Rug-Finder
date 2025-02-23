import numpy as np
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import StandardScaler
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

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