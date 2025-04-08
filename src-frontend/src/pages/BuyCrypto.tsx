import '../styles/BuyCrypto.css';
import React, { useState, useEffect } from 'react';
import { useNavigate, useLocation } from "react-router-dom";
import { useToast } from '../contexts/ToastContext';
import fetchPrice from '../components/fetchPrice';

import api from '../lib/api';


interface Holding {
  amount: number;
  name: string;
  symbol: string;
  value: number;
}

interface Wallet {
  name: string;
  balance: number;
  address: string;
  coin_symbol: string;
  fake_balance: string
  holdings: {
    [key: string]: Holding;
  };
}



const BuyCrypto = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const wallet = location.state?.wallet as Wallet;
  const [amountToBuy, setAmountToBuy] = useState("");
  const { priceData } = fetchPrice();
  const rate = priceData?.[wallet.coin_symbol === "BTC" ? "BTC-GBP" : "ETH-GBP"];
  const { showToast } = useToast();
  const [showTutorial, setShowTutorial] = useState<boolean>(false);
  const [detailsScreen, showDetailsScreen] = useState(false);

  const savedTheme = localStorage.getItem('theme');

  useEffect(() => {
    if (savedTheme === 'light')
      document.body.classList.add('light-mode');
    else
      document.body.classList.remove('light-mode');
  }, [savedTheme]);


  const buyAction = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!amountToBuy.trim() || parseFloat(amountToBuy) <= 0) {
      showToast("Please enter a valid amount greater than or equal to 0.00001.", "error");
      return;
    }

    showDetailsScreen(true);
  };

  const buyConfirm = async () => {
    try {
      const amount = parseFloat(amountToBuy);
  
      const platform = await window.api.getOS();
      if (platform === "darwin") {
        const response = await api.verifyBiometricForTransaction(wallet);
        if (!response.ok) {
          const data = await response.json();
          showToast(data.error || "Biometric verification failed", "error");
          return;
        }
      } else {
        const response = await api.verifyBiometricForTransaction(wallet);
        if (response.status !== 200) {
          showToast('Invalid Password or biometrics!', 'error');
          return;
        }
      }
  
      const result = await api.fakeBuy(wallet.name, amount);
      if (result.success) { 
        showToast("Purchase successful!", "success");
        console.log("Purchase recorded successfully!");
        navigate(-1);
      } else {
        showToast(result.error || "Purchase failed", "error");
      }
    } catch (err) {
      showToast("Failed to process purchase.", "error");
      console.error(err);
    }
  };



  if (detailsScreen) {
    return (
      <div className="confirm-modal-overlay">
        <div className="confirm-modal-content">
          <div className="confirm-header">
            <h2>Confirm details</h2>
          </div>
          <div>
            <p>Wallet: {wallet.name}</p>
            <p>Amount to purchase: {amountToBuy} {wallet?.coin_symbol}</p>
            <p>Total price: £{typeof Number(rate) === 'number' && amountToBuy ? (Number(rate) * parseFloat(amountToBuy)).toFixed(2) : '0.00'}</p>
          </div>
          <div className="confirmation-buttons">
            <button type="button" className="cancel-confirmation" onClick={() => showDetailsScreen(false)}>Cancel</button>
            <button type="button" className="confirm-transaction-button" onClick={() => buyConfirm()}>Confirm</button>
          </div>
        </div>
      </div>
    );
  }






  return (
    <div className="return-container">
      {showTutorial ?
        <div className="instructionBox">
          <button className="close-button" onClick={() => setShowTutorial(!showTutorial)}>
            ×
          </button>
          <p>Buy Crypto allows you to buy a quantity of the asset associated to the wallet and store it.</p>
          <p>
            Please enter the amount you wish to buy in asset terms, not GBP.
            The total price of the amount you wish to buy will be displayed in GBP.
            After confirming, you can purchase the asset successfully.
          </p>
        </div>
        : null}
      <form onSubmit={buyAction} className="buy-form">
        <div className="help-tutorial">
          <button type="button" className="tutorial-button" onClick={() => setShowTutorial(!showTutorial)}>?</button>
        </div>
        <label htmlFor="" className="main-label">Buy Crypto</label>
        <label htmlFor="buy-amount" id="buy-amountLabel">Enter Amount</label>
        <input type="number" min="0.00001" step="0.000001" onChange={(e) => setAmountToBuy(e.target.value)} name="amount" id="buy-amount" placeholder="Enter Amount" className="buyingInput" />
        <div id="buy-receive-amount">
          <p>Rate: 1 {wallet?.coin_symbol} = £{rate}</p>
        </div>
        <label htmlFor="receive-amount" id="receive-label">Total Price:</label>
        <div id="receive-amount">
          <p>£{typeof Number(rate) === 'number' && amountToBuy ? (Number(rate) * parseFloat(amountToBuy)).toFixed(2) : '0.00'}</p>
        </div>

        <div className="buttons">
          <button type="button" className="goBack" onClick={() => navigate(-1)}>Cancel</button>
          <button type="submit" className="buy-button">Buy</button>
        </div>
      </form>
    </div>
  );
};

export default BuyCrypto;