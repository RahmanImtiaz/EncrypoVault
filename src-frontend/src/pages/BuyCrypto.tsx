import '../styles/BuyCrypto.css';
import React, { useState } from 'react';

import { useNavigate } from "react-router-dom";

const BuyCrypto = () => {
  const navigate = useNavigate();
  const [selectedOption, setSelectedOption] = useState("");
  const [amountToSell, setAmountToSell] = useState("");
  /*const [amountToReceive, setAmountToReceive] = useState("");*/
  const [confirmMessage, setConfirmMessage] = useState("");

  const handleChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
      setSelectedOption(event.target.value);
  };

  const buyAction = async (e: React.FormEvent) => {
      e.preventDefault();
      
      if (!amountToSell.trim()) {
          setConfirmMessage("Please enter an amount to sell");
          return;
      }
      
  
      try {
        console.log("New contact added");
        setConfirmMessage("New contact added");
        // onRegister();
      } catch (err) {
          setConfirmMessage("Failed to add contact.");
        console.error(err);
      }
    };

  return (
      <div>
      <form onSubmit={buyAction} className="buy-form">
          <label htmlFor="" className="main-label">Buy Crypto</label>
          <label htmlFor="toBuy" id="buyLabel">Crypto Assets</label>
          <div className="toBuy">
              <select id="buy-crypto-dropdown" value={selectedOption} onChange={handleChange}>
                  <option value="">--Choose an option--</option>
                  <option value="Bitcoin">Bitcoin</option>
                  <option value="Ethereum">Ethereum</option>
                  <option value="Bitcoin Dogs">Bitcoin Dogs</option>
                  <option value="Hello">Hello</option>
              </select>
              <p>Rate: £1 = ... {selectedOption}</p>
          </div>
          <label htmlFor="buy-amount" id="buy-amountLabel">Enter Amount</label>
          <input type="text" onChange={(e) => setAmountToSell(e.target.value)} name="amount" id="buy-amount" placeholder="Enter Amount" className="buyingInput"/>
          <div id="buy-receive-amount">
              <p>Crypto Quantity you will receive: ...</p>
          </div>
          <div className="buttons">
              <button type="button" className="goBack" onClick={() => navigate(-1)}>Cancel</button>
              <button type="submit" className="buy-button">Buy</button>
          </div>
          {confirmMessage && <p className="error-message">{confirmMessage}</p>}
          </form>
      </div>
  );
};

export default BuyCrypto;