import React, { useEffect, useState } from 'react';
import axios from 'axios';
import '../styles/CryptoInfo.css';

const CryptoInfo = ({ cryptoToken }) => {
    const [price, setPrice] = useState(0);
    const [liquidity, setLiquidity] = useState(0);
    const [marketCap, setMarketCap] = useState(0);

    const formatUSD = (value) => {
        return new Intl.NumberFormat('en-US', {
            style: 'currency',
            currency: 'USD',
        }).format(value);
    };

  useEffect(() => {
    if (cryptoToken) {
      axios.get(`http://localhost:8000/api/token-price/?token=${cryptoToken}`)
        .then(res => {
            console.log(res.data.pairs[0]);
            setPrice(res.data.pairs[0].usdPrice);
            setLiquidity(res.data.pairs[0].liquidityUsd);
            // setMarketCap({marketCap: res.data[0].marketCapUsd});
        })
        .catch(err => {
            console.log(err);
        });
    }
  }, [cryptoToken, price, liquidity, marketCap]);

return (
    <div className="CryptoInfo-container-internal">
        <div className="CryptoInfo-box">
            <p>Price</p>
            <h3>{formatUSD(price)}</h3>
        </div>
        <div className="CryptoInfo-box">
            <p>Liquidity</p>
            <h3>{formatUSD(liquidity)}</h3>
        </div>
        <div className="CryptoInfo-box">
            <p>Market Cap</p>
            {/* <h3>{marketCap}</h3> */}
        </div>
    </div>
);
};

export default CryptoInfo;