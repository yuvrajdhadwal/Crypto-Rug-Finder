import React, { useEffect, useState } from 'react';
import axios from 'axios';
import '../styles/Sentiments.css';

const Sentiments = ({ cryptoToken, buttonNumber }) => {
  const [sentiments, setSentiments] = useState({});

  useEffect(() => {
    if (cryptoToken) {
      axios.get(`http://localhost:8000/api/get_sentiment/?query=${cryptoToken}`)
        .then(res => {
            setSentiments({
                overall: res.data.overall_sentiment,
                comment: res.data.overall_comment_sentiment,
                text: res.data.overall_text_sentiment,
                title: res.data.overall_title_sentiment,
            });
        })
        .catch(err => {
            console.log(err);
        });
    }
  }, [cryptoToken, buttonNumber]);

return (
    <div className="sentiments-container-internal">
        {sentiments.overall && sentiments.overall.length > 0 ? (
            <ul className="sentiments-list">
                <h2>Sentiment</h2>
                
                {!sentiments.overall.includes('Unbiased') && 
                <li className="sentiment">
                    <div className="sentiment-header">
                        <p className="sentiment-title">
                            🚩 {sentiments.overall}
                        </p>
                    </div>
                    <div className="sentiment-details">
                        Overall Sentiment
                    </div>
                </li>}

                {!sentiments.comment.includes('Unbiased') && 
                    <li className="sentiment">
                    <div className="sentiment-header">
                        <p className="sentiment-title">
                            🚩 {sentiments.comment}
                        </p>
                    </div>
                    <div className="sentiment-details">
                        Comments' Sentiment
                    </div>
                </li>}

                {!sentiments.text.includes('Unbiased') && 
                    <li className="sentiment">
                    <div className="sentiment-header">
                        <p className="sentiment-title">
                            🚩 {sentiments.text}
                        </p>
                    </div>
                    <div className="sentiment-details">
                        Text Sentiment
                    </div>
                </li>}

                {!sentiments.title.includes('Unbiased') && 
                    <li className="sentiment">
                    <div className="sentiment-header">
                        <p className="sentiment-title">
                            🚩 {sentiments.title}
                        </p>
                    </div>
                    <div className="sentiment-details">
                        Title Sentiment
                    </div>
                </li>}
            </ul>
        ) : (
            <p></p>
        )}
        {sentiments.overall && sentiments.comment && sentiments.text && sentiments.title &&
            sentiments.overall.includes('Unbiased') &&
            sentiments.comment.includes('Unbiased') &&
            sentiments.text.includes('Unbiased') &&
            sentiments.title.includes('Unbiased') && (
                <p>All sentiments are unbiased.</p>
        )}
    </div>
);
};

export default Sentiments;