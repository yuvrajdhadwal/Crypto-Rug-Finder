import React, { useEffect, useState } from 'react';
import axios from 'axios';
import '../styles/Notes.css';
import config from '../config';

const Notes = ({ cryptoToken }) => {
  const [honeypot, setHoneypot] = useState(false);
  const [hasQueried, setHasQueried] = useState(false);

  useEffect(() => {
    if (cryptoToken) {
      axios.get(`${config.baseURL}/api/honeypot/?token=${cryptoToken}&chain=eth`)
        .then(res => {
            setHoneypot(res.data.honeypotResult.isHoneypot);
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
            </ul>
        ) : (
            <p></p>
        )}
    </div>
);
};

export default Notes;