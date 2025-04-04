import '../styles/BuyCrypto.css';
import React, { useState, useEffect } from 'react';
import { useNavigate } from "react-router-dom";
import { useToast } from '../contexts/ToastContext';

const BuyCrypto = () => {
  const navigate = useNavigate();
  const [selectedOption, setSelectedOption] = useState("");
  const [amountToSell, setAmountToSell] = useState("");
  const [confirmMessage, setConfirmMessage] = useState("");
  const { showToast } = useToast();

  const savedTheme = localStorage.getItem('theme');

  useEffect(() => {
    if (savedTheme === 'light')
      document.body.classList.add('light-mode');
    else 
      document.body.classList.remove('light-mode');
  }, [savedTheme]);



  const handleChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
        setSelectedOption(event.target.value);
  };

  const buyAction = async (e: React.FormEvent) => {
        e.preventDefault();
        
        if (!selectedOption) {
            setConfirmMessage("Please select a cryptocurrency to buy.");
            showToast("Please select a cryptocurrency to buy.", "error");
            return;
        }

        if (!amountToSell.trim() || parseFloat(amountToSell) <= 0) {
            setConfirmMessage("Please enter a valid amount greater than £0.00.");
            showToast("Please enter a valid amount greater than £0.00.", "error");
            return;
        }

        try {
            console.log("Crypto purchase initiated.");
            setConfirmMessage("Purchase successful!");
            showToast("Purchase successful!", "success");
            // Implement the actual purchase logic here
        } catch (err) {
            setConfirmMessage("Transaction failed. Please try again.");
            showToast("Transaction failed. Please try again.", "error");
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
          <input type="number" min="0.01" step="0.000001" onChange={(e) => setAmountToSell(e.target.value)} name="amount" id="buy-amount" placeholder="Enter Amount" className="buyingInput"/>
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