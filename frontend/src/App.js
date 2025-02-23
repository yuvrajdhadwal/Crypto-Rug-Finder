import React from 'react';
import Header from './components/Header';
import CryptoNameInput from './components/CryptoNameInput';
import RedditPosts from './components/RedditPosts';
import Sentiments from './components/Sentiments';
import BotCheck from './components/BotCheck';
import CryptoInfo from './components/CryptoInfo';
import Notes from './components/Notes';

class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      cryptoName: null,
      buttonNumber: null,
      redditLoaded: false,
      refreshKey: Date.now(),
    };
  }

  componentDidMount() {
    window.addEventListener('cryptoNameSelected', this.handleCryptoNameSelected);
    window.addEventListener('redditLoaded', this.handleRedditLoaded);
  }

  componentWillUnmount() {
    window.removeEventListener('cryptoNameSelected', this.handleCryptoNameSelected);
    window.removeEventListener('redditLoaded', this.handleRedditLoaded);
  }

  handleCryptoNameSelected = (event) => {
    const { cryptoName, cryptoToken } = event.detail;
    this.setState({ cryptoName, cryptoToken });
    this.setState({ redditLoaded: false });
    this.setState({ refreshKey: Date.now() });
  };

  handleRedditLoaded = () => {
    this.setState({ redditLoaded: true });
    this.setState({ key: Date.now() });
  }

  render() {
    const { cryptoName, cryptoToken, redditLoaded, refreshKey } = this.state;
    return (
      <div>
      <Header />
      <CryptoNameInput />
      {cryptoName ? (
        <div className="reddit-and-sentiments-container">
        <RedditPosts cryptoName={cryptoName} refreshKey={refreshKey} />
        {redditLoaded ? (
          <span>
          <Sentiments cryptoName={cryptoName} />
          <Notes cryptoToken={cryptoToken} />
          <BotCheck cryptoName={cryptoName} />
          </span>
        ) : (
          <p>Loading...</p>
        )}
        <CryptoInfo cryptoToken={cryptoToken} />
        </div>
      ) : (
        <p>Please select a cryptocurrency.</p>
      )}
      </div>
    );
  }
}

export default App;