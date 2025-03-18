from dotenv import load_dotenv
import os
from atproto import Client

load_dotenv()

client = Client()
client.login(os.getenv('BLUESKY_USERNAME'), os.getenv('BLUESKY_PASSWORD'))

# post = client.send_post('Hello world! I posted this via the Python SDK.')


search_term = 'Musk'
response = client.app.bsky.feed.search_posts({'q': search_term, 'limit': 100})

for post in response['posts']:
    print(f"Author: {post['author']['handle']}")
    print(f"Content: {post['record']['text']}")
    print("-------------------------------------------------")


print(len(response['posts']))