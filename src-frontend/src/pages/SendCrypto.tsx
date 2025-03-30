import '../styles/SendCrypto.css';
import React, { useState } from 'react';

import { useNavigate } from "react-router-dom";

const SendCrypto = () => {
  const navigate = useNavigate();
  const [selectedOption, setSelectedOption] = useState("");
  const [amountToSend, setAmountToSend] = useState("");
  /*const [amountToReceive, setAmountToReceive] = useState("");*/
  const [confirmMessage, setConfirmMessage] = useState("");

  const handleChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
      setSelectedOption(event.target.value);
  };

  const sellAction = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!amountToSend.trim()) {
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
        <form onSubmit={sellAction} className="send-form">
            <label htmlFor="" className="main-label">Send Crypto</label>
            <label htmlFor="toSend" id="sendLabel">Crypto Assets</label>
            <div className="toSend">
                <select id="crypto-dropdown" value={selectedOption} onChange={handleChange}>
                    <option value="">--Choose an option--</option>
                    <option value="Bitcoin">Bitcoin</option>
                    <option value="Ethereum">Ethereum</option>
                    <option value="Bitcoin Dogs">Bitcoin Dogs</option>
                    <option value="Hello">Hello</option>
                </select>
                <input type="text" onChange={(e) => setAmountToSend(e.target.value)} name="amount" id="amount" placeholder="Enter Amount" className="sellingInput"/>
            </div>
            <div className="information">
                <p>Total Owned: ...</p>
                <p>Rate: 1 {selectedOption} = "£..."</p>
            </div>
            <label htmlFor="contact-options" id="contacts">Choose Contact</label>
            <div id="contact-options">
                <button className="contact-option-button">New</button>
                <button className="contact-option-button">Existing</button>
                <button className="contact-option-button">QR code</button>
            </div>
            <div className="buttons">
                <button type="button" className="goBack" onClick={() => navigate(-1)}>Cancel</button>
                <button type="submit" className="send-button">Sell</button>
            </div>
            {confirmMessage && <p className="error-message">{confirmMessage}</p>}
            </form>
        </div>
    );
};

export default SendCrypto;