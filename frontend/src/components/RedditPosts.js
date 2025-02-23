import React, { useEffect, useState } from 'react';
import axios from 'axios';
import '../styles/RedditPosts.css';
import config from '../config';

const RedditPosts = ({ cryptoName, refreshKey }) => {
  const [posts, setPosts] = useState([]);

  useEffect(() => {
      if (cryptoName) {
      setPosts([]);
      axios.get(`${config.baseURL}/api/reddit/?query=${cryptoName}`)
        .then(res => {
          setPosts(res.data.posts);
            setTimeout(() => {
                window.dispatchEvent(new Event('redditLoaded'));
            }, 100);
        })
        .catch(err => {
          console.log(err);
        });
    }
  }, [cryptoName, refreshKey]);

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