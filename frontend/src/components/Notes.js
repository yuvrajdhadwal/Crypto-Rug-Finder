import React, { useEffect, useState } from 'react';
import axios from 'axios';
import '../styles/Notes.css';
import config from '../config';

const Notes = ({ cryptoToken }) => {
  const [honeypot, setHoneypot] = useState(false);
  const [hasQueried, setHasQueried] = useState(false);
  const [rugpull, setRugpull] = useState(false);

  useEffect(() => {
    if (cryptoToken) {
      setHasQueried(false);

        // Honeypot
      axios.get(`${config.baseURL}/api/honeypot/?token=${cryptoToken}&chain=eth`)
        .then(res => {
            setHoneypot(res.data.honeypotResult.isHoneypot);
        })
        .catch(err => {
            console.log(err);
        });

        // Rugpull prediction
        axios.post(`${config.baseURL}/api/predict-rugpull/`, {
            token_address: cryptoToken
        }, {
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(res => {
            setRugpull(res.data.prediction === 1);
            setHasQueried(true);
        })
        .catch(err => {
            console.log(err);
        });
    }
  }, [cryptoToken]);

return (
    <div className="notes-container-internal">
        {hasQueried ? (
            <ul className="notes-list">
                <h2>Notes</h2>
                
                {honeypot &&
                <li className="note bad">
                    <div>
                        <p className="note-title">
                            🍯 Honeypot Detected!
                        </p>
                    </div>
                </li>}
                {!honeypot &&
                <li className="note good">
                    <div>
                        <p className="note-title">
                            🍯 Not a honeypot.
                        </p>
                    </div>
                </li>}

                {rugpull &&
                <li className="note bad">
                    <div>
                        <p className="note-title">
                            🚨 Prediction: Rugpull
                        </p>
                    </div>
                </li>}
                {!rugpull &&
                <li className="note good">
                    <div>
                        <p className="note-title">
                            🚨 Prediction: Not a rugpull
                        </p>
                    </div>
                </li>}
            </ul>
        ) : (
            <p></p>
        )}
    </div>
);
};

export default Notes;