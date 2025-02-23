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
    window.addEventListener('redditLoaded', this.hanldeRedditLoaded);
  }

  componentWillUnmount() {
    window.removeEventListener('cryptoNameSelected', this.handleCryptoNameSelected);
    window.removeEventListener('redditLoaded', this.hanldeRedditLoaded);
  }

  handleCryptoNameSelected = (event) => {
    const { cryptoName, buttonNumber } = event.detail;
    this.setState({ cryptoName, buttonNumber });
    this.setState({ redditLoaded: false });
  };

  hanldeRedditLoaded = () => {
    this.setState({ redditLoaded: true });
  }

  render() {
    const { cryptoName, cryptoToken, buttonNumber, redditLoaded } = this.state;
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
                <CryptoInfo cryptoToken={'0x3593D125a4f7849a1B059E64F4517A86Dd60c95d'} />
              </span>
            )}
          </div>
        )}
      </div>
    );
  }
}

export default App;