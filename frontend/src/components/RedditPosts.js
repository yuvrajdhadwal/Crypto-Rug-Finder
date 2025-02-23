import React, { useEffect, useState } from 'react';
import axios from 'axios';
import '../styles/RedditPosts.css';

const RedditPosts = ({ cryptoToken }) => {
  const [posts, setPosts] = useState([]);

  useEffect(() => {
    if (cryptoToken) {
      axios.get(`http://localhost:8000/api/reddit/?query=${cryptoToken}`)
        .then(res => {
          setPosts(res.data.posts);
        })
        .catch(err => {
          console.log(err);
        });
    }
  }, [cryptoToken]);

return (
    <div className="reddit-posts-container-internal">
        {posts.length > 0 ? (
            <ul className="reddit-posts-list">
                <h2>Reddit Posts</h2>
                {posts.map((post, index) => (
                    <li key={index} className="reddit-post">
                        <div className="reddit-post-header">
                            <a href={post.url} target="_blank" rel="noopener noreferrer" className="reddit-post-title">
                                {post.title}
                            </a>
                        </div>
                        <div className="reddit-post-details">
                            <span className="reddit-post-subreddit">r/{post.subreddit} • </span>
                            <span className="reddit-post-author">Posted by u/{post.post_author} • </span>
                            <span className="reddit-post-date">{new Date(post.created_utc * 1000).toLocaleDateString()}</span>
                        </div>
                        <div className="reddit-post-content">
                            {post.text ? post.text.substring(0, 100) + '...' : 'No content available'}
                        </div>
                    </li>
                ))}
            </ul>
        ) : (
            <p></p>
        )}
    </div>
);
};

export default RedditPosts;