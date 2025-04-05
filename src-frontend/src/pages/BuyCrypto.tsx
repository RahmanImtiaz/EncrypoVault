import '../styles/BuyCrypto.css';
import React, { useState, useEffect } from 'react';
import { useNavigate, useLocation } from "react-router-dom";
import { useToast } from '../contexts/ToastContext';
import useCryptoPrice from '../components/fetchPrice';


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
    holdings: {
      [key: string]: Holding;
    };
  }

  interface PriceData {
    market_data?: {
      current_price: {
        gbp: number;
        [key: string]: number;
      };
    };
  }



const BuyCrypto = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const wallet = location.state?.wallet as Wallet;
  const [amountToBuy, setAmountToBuy] = useState("");
  //const [confirmMessage, setConfirmMessage] = useState("");
  const { priceData } = useCryptoPrice() as { priceData: PriceData | null };
  const rate = priceData?.market_data?.current_price.gbp;
  const { showToast } = useToast();
  const [showTutorial, setShowTutorial] = useState<boolean>(false);

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
            //setConfirmMessage("Please enter a valid amount greater than £0.00.");
            showToast("Please enter a valid amount greater than £0.00.", "error");
            return;
        }

        try {
            console.log("Crypto purchase initiated.");
            //setConfirmMessage("Purchase successful!");
            showToast("Purchase successful!", "success");
            // Implement the actual purchase logic here
        } catch (err) {
            //setConfirmMessage("Transaction failed. Please try again.");
            showToast("Transaction failed. Please try again.", "error");
            console.error(err);
        }
    };

  return (
    <div className="return-container">
      {showTutorial?
        <div className="instructionBox">
          <button className="close-button" onClick={() => setShowTutorial(!showTutorial)}>
              ×
          </button>
          <p>Buy Crypto allows you to buy a quantity of the asset associated to the wallet and store it.
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
        <input type="number" min="0.00001" step="0.000001" onChange={(e) => setAmountToBuy(e.target.value)} name="amount" id="buy-amount" placeholder="Enter Amount" className="buyingInput"/>
        <div id="buy-receive-amount">
          <p>Rate: 1 {wallet?.coin_symbol} = £{typeof rate === 'number' ? rate.toFixed(2) : rate}</p>
        </div>
        <label htmlFor="receive-amount" id="receive-label">Total Price:</label>
        <div id="receive-amount">
          <p>£{typeof rate === 'number' && amountToBuy ? (rate * parseFloat(amountToBuy)).toFixed(2) : '0.00'}</p>
        </div>
          
        <div className="buttons">
          <button type="button" className="goBack" onClick={() => navigate(-1)}>Cancel</button>
          <button type="submit" className="buy-button">Buy</button>
        </div>
        {/*{confirmMessage && <p className="error-message">{confirmMessage}</p>}*/}
      </form>
    </div>
  );
};

export default BuyCrypto;