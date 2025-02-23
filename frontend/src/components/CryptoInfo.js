import React, { useEffect, useState } from 'react';
import axios from 'axios';
import '../styles/CryptoInfo.css';
import config from '../config';

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

    const formatNum = (value) => {
        return new Intl.NumberFormat('en-US').format(value);
    }

  useEffect(() => {
    if (cryptoToken) {

        // Price, Liquidity
      axios.get(`${config.baseURL}/api/token-price/?address=${cryptoToken}`)
        .then(res => {
            setPrice(res.data.pairs[0].usd_price);
            setLiquidity(res.data.pairs[0].liquidity_usd);
        })
        .catch(err => {
            console.log(err);
        });

        // Market Cap
        axios.get(`${config.baseURL}/api/market-data/?address=${cryptoToken}`)
            .then(res => {
                if (res.data['market_cap']) {
                    setMarketCap(res.data['market_cap']);
                }
            })
            .catch(err => {
                console.log(err);
            });


    }
  }, [cryptoToken, price, liquidity, marketCap]);

return (
    <div className="CryptoInfo-container-internal">
        {price ? (
            <>
                <div className="CryptoInfo-box">
                    <p>Price</p>
                    <h3>{formatUSD(price)}</h3>
                </div>
                <div className="CryptoInfo-box">
                    <p>Liquidity</p>
                    <h3>{formatNum(liquidity)}</h3>
                </div>
                <div className="CryptoInfo-box">
                    <p>Market Cap</p>
                    <h3>{formatUSD(marketCap)}</h3>
                </div>
            </>
        ) : (
            <p></p>
        )}
    </div>
);
};

export default CryptoInfo;