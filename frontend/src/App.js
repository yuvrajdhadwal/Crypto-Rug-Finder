import React from 'react';
import Header from './components/Header';
import CryptoTokenInput from './components/CryptoTokenInput';
import RedditPosts from './components/RedditPosts';
import Sentiments from './components/Sentiments';
import BotCheck from './components/BotCheck';

class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      cryptoToken: null,
      buttonNumber: null,
    };
  }

  componentDidMount() {
    window.addEventListener('cryptoTokenSelected', this.handleCryptoTokenSelected);
  }

  componentWillUnmount() {
    window.removeEventListener('cryptoTokenSelected', this.handleCryptoTokenSelected);
  }

  handleCryptoTokenSelected = (event) => {
    const { cryptoToken, buttonNumber } = event.detail;
    this.setState({ cryptoToken, buttonNumber });
  };

  render() {
    const { cryptoToken, buttonNumber } = this.state;
    return (
      <div>
        <Header />
        <CryptoTokenInput />
        {cryptoToken && (
          <div className="reddit-and-sentiments-container">
            <RedditPosts cryptoToken={cryptoToken} />
            <Sentiments cryptoToken={cryptoToken} />
            <BotCheck cryptoToken={cryptoToken} />
          </div>
        )}
      </div>
    );
  }
}

export default App;