import numpy as np
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from ..models import CryptoTokenSpam

# Common SPAM keywords
SPAM_KEYWORDS = {
    'airdrop', '100x', 'pump', 'moon',
    'profit', 'easy', 'DOGE', "diamond", "hold", 
    'WAGMI', 'NGMI', 'paper', 'Lambo', 'Lamborghini',
    'mooning', 'bear', 'bull', 'Shitcoin', 'HODL', 'FOMO',
    'FUD', 'wen', 'whale', 'p&d',
}

def extract_features(texts):
    analyzer = SentimentIntensityAnalyzer()
    vectorizer = TfidfVectorizer(max_features=500, stop_words="english")

    # compute tf-idf matrix
    tfidf_matrix = vectorizer.fit_transform(texts).toarray()

    data = []
    for i, text in enumerate(texts):
        sentiment = analyzer.polarity_scores(text)["compound"]
        text_length = len(text)
        num_links = len(re.findall(r'http[s]?://', text))  # Count URLs
        spam_word_count = sum(1 for word in text.lower().split() if word in SPAM_KEYWORDS)

        # Combine all features
        features = [
            text_length, sentiment, num_links, spam_word_count,
        ] + list(tfidf_matrix[i])

        data.append(features)
    
    return np.array(data)


def detect_spam(texts, n_clusters=2):
    """Using k-means clustering to catch potential bot/spam activity"""
    
    features = extract_features(texts)

    scaler = StandardScaler()
    features_scaled = scaler.fit_transform(features)

    kmeans = KMeans(n_clusters=n_clusters, random_state=8152005, n_init=10)
    clusters = kmeans.fit_predict(features_scaled)

    cluster_means = features_scaled.mean(axis=0)
    spam_cluster = np.argmax(cluster_means[4])  # Spam keywords as key identifier

    spam_labels = [clusters[i] == spam_cluster for i in range(len(texts))]

    return spam_labels

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
