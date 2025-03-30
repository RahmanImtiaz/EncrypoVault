// Portfolio.tsx
import React from 'react';
//import '../styles/Setting.css';
import '../styles/WalletInfo.css';
import { useNavigate } from "react-router-dom";
import { useState } from "react";

const Setting: React.FC = () => {
  const navigate = useNavigate();
  const [cryptoDetailsDisplay, setCryptoDetailsDisplay] = useState(false);
  const [transactionDetails, setTransactionDetails] = useState(false);

  const showCryptoDetails = () => {
    setCryptoDetailsDisplay(!cryptoDetailsDisplay);
  }

  const showCryptoTransactions = () => {
    setTransactionDetails(!transactionDetails);
  }



  return (
    <div className="WalletInfo-container">
      <div className="balanceContainer-wallet">
        <div className="balanceContainer-heading">
          <h2>Wallet Name</h2> {/*To be changed later and replaced with the name of the wallet*/}
        </div>
        <div className="balanceContainer-amount">
          <p>£53.00</p> {/*To be changed later and replaced with the amount of money*/}
        </div>
        <div className="balanceContainer-currency">
          <select id="currency-dropdown">
            <option value="GBP">GBP</option>
            <option value="USD">USD</option>
            <option value="Yuan">Yuan</option>
          </select>
        </div>
      </div>
      <div className="actionButtons">
          <button className="actionButton" onClick={() => navigate("/buy")}>Buy Crypto</button>
          <button className="actionButton" onClick={() => navigate("/sell")}>Sell Crypto</button>
          <button className="actionButton" onClick={() => navigate("/send")}>Send Crypto</button>
          <button className="actionButton" onClick={() => navigate("/receive")}>Receive Crypto</button>
      </div>
      <button onClick={showCryptoDetails} className="more-info-buttons">Crypto Assets</button>
      {cryptoDetailsDisplay? "Information to be added" : null}
      <button onClick={showCryptoTransactions} className="more-info-buttons">Recent Transactions</button>
      {transactionDetails? "Information to be added" : null}
    </div>
  );
};

export default Setting;