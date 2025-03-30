import '../styles/SellCrypto.css';
import React, { useState } from 'react';
import { useNavigate } from "react-router-dom";


export const SellCrypto = () => {
    const navigate = useNavigate();
    const [selectedOption, setSelectedOption] = useState("");
    const [amountToSell, setAmountToSell] = useState("");
    /*const [amountToReceive, setAmountToReceive] = useState("");*/
    const [confirmMessage, setConfirmMessage] = useState("");

    const handleChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
        setSelectedOption(event.target.value);
    };

    const sellAction = async (e: React.FormEvent) => {
        e.preventDefault();
        
        if (!selectedOption) {
            setConfirmMessage("Please select a cryptocurrency to sell.");
            return;
        }

        if (!amountToSell.trim() || parseFloat(amountToSell) <= 0) {
            setConfirmMessage("Please enter a valid amount greater than 0.00001.");
            return;
        }

        try {
            console.log("Crypto selling initiated.");
            setConfirmMessage("Selling successful!");
            // Implement the actual purchase logic here
        } catch (err) {
            setConfirmMessage("Transaction failed. Please try again.");
            console.error(err);
        }
      };

    return (
        <div>
        <form onSubmit={sellAction} className="sell-form">
            <label htmlFor="" className="main-label">Sell Crypto</label>
            <label htmlFor="toSell" id="sellLabel">Crypto Assets</label>
            <div className="toSell">
                <select id="crypto-dropdown" value={selectedOption} onChange={handleChange}>
                    <option value="">--Choose an option--</option>
                    <option value="Bitcoin">Bitcoin</option>
                    <option value="Ethereum">Ethereum</option>
                    <option value="Bitcoin Dogs">Bitcoin Dogs</option>
                    <option value="Hello">Hello</option>
                </select>
                <input type="text" min="0.00001" step="0.000001" onChange={(e) => setAmountToSell(e.target.value)} name="amount" id="amount" placeholder="Enter Amount" className="sellingInput"/>
            </div>
            <div className="information">
                <p>Total Owned: ...</p>
                <p>Rate: 1 {selectedOption} = "£..."</p>
            </div>
            <label htmlFor="receive-amount" id="receive-label">You will Receive</label>
            <div id="receive-amount">
                <p>£25.43</p>
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

export default SellCrypto;