import React, { useState } from 'react';
import '../styles/CryptoTokenInput.css';

const CryptoTokenInput = () => {
  const [highlightedButton, setHighlightedButton] = useState(null);
  const [cryptoToken, setcryptoToken] = useState('');

  const handleButtonClick = (buttonNumber) => {
    setHighlightedButton(buttonNumber);

    // Begin querying
    const event = new CustomEvent('cryptoTokenSelected', { detail: { cryptoToken, buttonNumber } });
    window.dispatchEvent(event);
  };

  return (
    <div className="crypto-token-input">
      <input
        type="text"
        id="crypto-token"
        name="crypto-token"
        placeholder="Enter a Crypto Token"
        maxLength="100"
        onInput={(e) => {
          if (!e.target.value.startsWith('$')) {
            e.target.value = '$' + e.target.value.toUpperCase();
          } else {
            e.target.value = e.target.value.toUpperCase();
          }
          setcryptoToken(e.target.value.slice(1));
          setHighlightedButton(null);
        }}
      />

      <div className="toggle-buttons">
        <button
          className={highlightedButton === 1 ? 'highlighted' : ''}
          onClick={() => handleButtonClick(1)}
        >
          Etherium (ETH)
        </button>
        <button
          className={highlightedButton === 2 ? 'highlighted' : ''}
          onClick={() => handleButtonClick(2)}
        >
          Solana (SOL)
        </button>
      </div>
    </div>
  );
};

export default CryptoTokenInput;