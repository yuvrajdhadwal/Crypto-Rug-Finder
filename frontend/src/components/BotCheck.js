import React, { useEffect, useState } from 'react';
import axios from 'axios';
import '../styles/BotCheck.css';
import { Doughnut } from 'react-chartjs-2';
import { Chart, ArcElement, Title } from 'chart.js';
import ChartDataLabels from 'chartjs-plugin-datalabels';

Chart.register(ArcElement, ChartDataLabels, Title);

const centerTitlePlugin = {
  id: 'centerTitle',
  beforeDraw: function(chart) {
    const ctx = chart.ctx;
    const width = chart.width;
    const height = chart.height;
    const title = chart.options.plugins.title.text;
    ctx.restore();
    const fontSize = (height / 200).toFixed(2);
    ctx.font = `${fontSize}em sans-serif`;
    ctx.textBaseline = 'middle';
    const textX = Math.round((width - ctx.measureText(title).width) / 2);
    const textY = height / 2;
    ctx.fillText(title, textX, textY);
    ctx.save();
  }
};

Chart.register(centerTitlePlugin);

const BotCheck = ({ cryptoName }) => {
  const [post_data, setPostData] = useState(null);
  const [comment_data, setCommentData] = useState(null);

  useEffect(() => {
    if (cryptoName) {
      axios.get(`http://localhost:8000/api/bot_check/?query=${cryptoName}`)
        .then(res => {
            const post_spam = res.data['Post Spam'];
            const comment_spam = res.data['Comment Spam'];
            setPostData({
                labels: ['Bots', 'Humans'],
                datasets: [
                    {
                        data: [post_spam, 100 - post_spam],
                        backgroundColor: ['#FF5555', '#36A2EB'],
                        hoverBackgroundColor: ['#FF6384', '#36BBBB'],
                    },
                ],
            });
            setCommentData({
                labels: ['Bots', 'Humans'],
                datasets: [
                    {
                        data: [comment_spam, 100 - comment_spam],
                        backgroundColor: ['#FF5555', '#36A2EB'],
                        hoverBackgroundColor: ['#FF6384', '#36BBBB'],
                    },
                ],
            });

        })
        .catch(err => {
            console.log(err);
        });
    }
  }, [cryptoName]);

  const options = {
    plugins: {
      datalabels: {
        formatter: (value, context) => {
          const label = context.chart.data.labels[context.dataIndex];
          const total = context.chart.data.datasets[0].data.reduce((acc, curr) => acc + curr, 0);
          const percentage = ((value / total) * 100).toFixed(1) + '%';
          return `${label}:\n${percentage}`;
        },
        color: '#fff',
      },
      title: {
        display: false, // Disable the default title plugin
        text: 'Posts',
      },
      centerTitle: {
        text: 'Comments',
      },
    },
  };

  const commentOptions = {
    ...options,
    plugins: {
      ...options.plugins,
      title: {
        text: 'Comments',
      },
      centerTitle: {
        text: 'Comments',
      },
    },
  };

  return (
      <div className="sentiments-container-internal">
        <br />
        {post_data ? (
            <ul>
                <h2>Bot Activity</h2>
                <div className="donut-chart">
                    <Doughnut data={post_data} options={options} />
                </div>
                <div className="donut-chart">
                    <Doughnut data={comment_data} options={commentOptions} />
                </div>
            </ul>
        ) : (
            <p>Loading...</p>
        )}
    </div>
  );
};

export default BotCheck;