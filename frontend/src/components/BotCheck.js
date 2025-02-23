import React, { useEffect, useState } from 'react';
import axios from 'axios';
import '../styles/Sentiments.css';
import { Doughnut } from 'react-chartjs-2';

const Sentiments = ({ cryptoToken, buttonNumber }) => {
  const [data, setData] = useState({});

  useEffect(() => {
    if (cryptoToken) {
      axios.get(`http://localhost:8000/api/bot_check/?query=${cryptoToken}`)
        .then(res => {
            console.log(res.data);
            const post_spam = res.data['Post Spam'];
            const comment_spam = res.data['Comment Spam'];
            setData({
                labels: ['Bot Activity', 'Human Activity'],
                datasets: [
                    {
                        data: [post_spam, 100 - post_spam],
                        backgroundColor: ['#FF6384', '#36A2EB'],
                        hoverBackgroundColor: ['#FF6384', '#36A2EB'],
                    },
                ],
            });

        })
        .catch(err => {
            console.log(err);
        });
    }
  }, [cryptoToken, buttonNumber]);

return (
    <div className="sentiments-container-internal">
        {data ? (
            <ul className="sentiments-list">
                <h2>Bot Activity</h2>
            
                {data}
                {/* <Doughnut data={data} /> */}
                

            </ul>
        ) : (
            <p></p>
        )}
    </div>
);
};

export default Sentiments;