import React from 'react';
import Header from './components/Header';
import CryptoNameInput from './components/CryptoNameInput';
import RedditPosts from './components/RedditPosts';
import Sentiments from './components/Sentiments';
import BotCheck from './components/BotCheck';
import CryptoInfo from './components/CryptoInfo';

class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      cryptoName: null,
      buttonNumber: null,
      redditLoaded: false,
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
  };

  handleRedditLoaded = () => {
    this.setState({ redditLoaded: true });
  }

  render() {
    const { cryptoName, cryptoToken, redditLoaded } = this.state;
    return (
      <div>
        <Header />
        <CryptoNameInput />
        {cryptoName && (
          <div className="reddit-and-sentiments-container">
            <RedditPosts cryptoName={cryptoName} />
            {redditLoaded && (
              <span>
                <span>
                  <Sentiments cryptoName={cryptoName} />
                  <BotCheck cryptoName={cryptoName} />
                </span>
            </span>
            )}
            <CryptoInfo cryptoToken={cryptoToken} />
          </div>
        )}
      </div>
    );
  }
}

export default App;