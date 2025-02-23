import React, { useEffect, useState } from 'react';
import axios from 'axios';
import '../styles/CryptoInfo.css';

const CryptoInfo = ({ cryptoToken }) => {
  const [CryptoInfo, setCryptoInfo] = useState({});

  useEffect(() => {
    if (cryptoToken) {
      axios.get(`http://localhost:8000/api/token-price/?query=${cryptoToken}&chain=mainnet`)
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
        test
    </div>
);
};

export default CryptoInfo;