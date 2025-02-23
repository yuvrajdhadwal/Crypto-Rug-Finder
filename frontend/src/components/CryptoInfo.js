import React, { useEffect, useState } from 'react';
import axios from 'axios';
import '../styles/CryptoInfo.css';

const CryptoInfo = ({ cryptoToken }) => {
  const [CryptoInfo, setCryptoInfo] = useState({});

  useEffect(() => {
    if (cryptoToken) {
      axios.get(`http://localhost:8000/api/token-price/?token=${cryptoToken}`)
        .then(res => {
            console.log(res.data);
        })
        .catch(err => {
            console.log(err);
        });
    }
  }, [cryptoToken]);

return (
    <div className="CryptoInfo-container-internal">
        <div className="CryptoInfo-box">
            <h3>Price</h3>
            <p>{CryptoInfo.price}</p>
        </div>
        <div className="CryptoInfo-box">
            <h3>Liquidity</h3>
            <p>{CryptoInfo.liquidity}</p>
        </div>
        <div className="CryptoInfo-box">
            <h3>Market Cap</h3>
            <p>{CryptoInfo.marketCap}</p>
        </div>
    </div>
);
};

export default CryptoInfo;