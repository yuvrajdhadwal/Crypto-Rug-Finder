from ..models import RedditPost, RedditComment

def fetch_subreddit_posts(subreddit_name, reddit_query, limit, max_comments, query, reddit):
    """Fetch posts from a single subreddit and store them in the database."""
    results = []
    subreddit = reddit.subreddit(subreddit_name)

    for post in subreddit.search(query=reddit_query, syntax="lucene", limit=limit):
        post_author = post.author.name if post.author else "Unknown"

        # Check if the post is already stored
        reddit_post, created = RedditPost.objects.get_or_create(
            url=post.url,
            defaults={
                "crypto_token": query,
                "subreddit": subreddit_name,
                "title": post.title,
                "text": post.selftext,
                "upvotes": post.score,
                "comments_count": post.num_comments,
                "post_author": post_author,
            }
        )

        # Fetch comments in parallel if post is new
        if created:
            post.comments.replace_more(limit=0)  # Remove "More Comments" button
            RedditComment.objects.bulk_create([
                RedditComment(
                    post=reddit_post,
                    author=comment.author.name if comment.author else "Unknown",
                    text=comment.body,
                    upvotes=comment.score
                ) for comment in post.comments[:max_comments]
            ])

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

    return results
