import React, { useState } from 'react';
import '../styles/CryptoNameInput.css';

const CryptoNameInput = () => {
  // const [highlightedButton, setHighlightedButton] = useState(null);
  const [cryptoName, setcryptoName] = useState('');
  const [cryptoToken, setcryptoToken] = useState('');

  const handleButtonClick = (buttonNumber) => {
    // setHighlightedButton(buttonNumber);

    // Begin querying
    const event = new CustomEvent('cryptoNameSelected', { detail: { cryptoName, cryptoToken } });
    window.dispatchEvent(event);
  };

  return (
    <div className="crypto-token-input">
      <input
        type="text"
        id="crypto-name"
        name="crypto-name"
        placeholder="Enter a Crypto Name"
        maxLength="100"
        onKeyDown={(e) => {
          if (e.key === 'Enter') {
            handleButtonClick(null);
          }
        }}
        onInput={(e) => {
          if (!e.target.value.startsWith('$')) {
            e.target.value = '$' + e.target.value.toUpperCase();
          } else {
            e.target.value = e.target.value.toUpperCase();
          }
          setcryptoName(e.target.value.slice(1));
          // setHighlightedButton(null);
        }}
      />
      <input
        type="text"
        id="crypto-token"
        name="crypto-token"
        placeholder="Enter a Crypto Token"
        maxLength="100"
        onKeyDown={(e) => {
          if (e.key === 'Enter') {
            handleButtonClick(null);
          }
        }}
        onInput={(e) => {
          setcryptoToken(e.target.value);
          // setHighlightedButton(null);
        }}
      />

      {/* <div className="toggle-buttons">
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
      </div> */}
    </div>
  );
};

export default CryptoNameInput;