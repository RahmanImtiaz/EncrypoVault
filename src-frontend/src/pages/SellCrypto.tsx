import '../styles/SellCrypto.css';
import React, { useState, useEffect } from 'react';
import { useNavigate, useLocation } from "react-router-dom";
import { useToast } from '../contexts/ToastContext';
import fetchPrice from '../components/fetchPrice';
import api from '../lib/api';
import { PublicKeyCredentialRequestOptionsJSON, startAuthentication } from '@simplewebauthn/browser';



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



export const SellCrypto = () => {
    const navigate = useNavigate();
    const location = useLocation();
    const wallet = location.state?.wallet as Wallet;
    const [amountToSell, setAmountToSell] = useState("");
    const { showToast } = useToast();
    const { priceData } = fetchPrice();
    const rate = priceData?.[wallet.coin_symbol === "BTC" ? "BTC-GBP" : "ETH-GBP"];
    const savedTheme = localStorage.getItem('theme');
    const [showTutorial, setShowTutorial] = useState<boolean>(false);
    const [detailsScreen, showDetailsScreen] = useState(false);

    useEffect(() => {
        if (savedTheme === 'light')
            document.body.classList.add('light-mode');
        else
            document.body.classList.remove('light-mode');
    }, [savedTheme]);


    const sellAction = async (e: React.FormEvent) => {
        e.preventDefault();

        if (!amountToSell.trim() || parseFloat(amountToSell) <= 0) {
            showToast("Please enter a valid amount greater than 0.00001.", "error");
            return;
        }

        {/*}
        if (parseFloat(amountToSell) > wallet.balance) {
            showToast("Insufficient balance. Please enter a valid amount up to or equal to your balance.", "error");
            return;
        }*/}

        showDetailsScreen(true);
    };

    const sellConfirm = async () => {
        try {
            const platform = await window.api.getOS()
            if (platform == "darwin") {
                // Trigger biometric verification
                const response = await api.verifyBiometricForTransaction(wallet);

                if (!response.ok) {
                    const data = await response.json();
                    showToast(data.error || "Biometric verification failed", "error");
                    return;
                }
            } else {
                const authData: PublicKeyCredentialRequestOptionsJSON = await window.api.getWebauthnLoginOpts() as unknown as PublicKeyCredentialRequestOptionsJSON
                // const webauthnResponse = await startAuthentication({ optionsJSON: authData, useBrowserAutofill: false })
                const response = await api.verifyBiometricForTransaction(wallet);

                if (response.status !== 200) {
                    showToast('Invalid Password or biometrics!', 'error');
                    return;
                }
            }

            console.log("Crypto selling initiated.");
            showToast("Selling successful!", "success");
            navigate(-1);
        } catch (err) {
            showToast("Transaction failed. Please try again.", "error");
            console.error(err);
        }
    }


    if (detailsScreen) {
        return (
            <div className="confirm-modal-overlay">
                <div className="confirm-modal-content">
                    <div className="confirm-header">
                        <h2>Confirm details</h2>
                    </div>
                    <div>
                        <p>Wallet: {wallet.name}</p>
                        <p>Amount to sell: {amountToSell} {wallet?.coin_symbol}</p>
                        <p>You will receive: £{typeof Number(rate) === 'number' && amountToSell ? (Number(rate) * parseFloat(amountToSell)).toFixed(2) : '0.00'}</p>
                    </div>
                    <div className="confirmation-buttons">
                        <button type="button" className="cancel-confirmation" onClick={() => showDetailsScreen(false)}>Cancel</button>
                        <button type="button" className="confirm-transaction-button" onClick={() => sellConfirm()}>Confirm</button>
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
                    <p>Sell Crypto allows you to sell a quantity of your asset for money in return.</p>
                    <p>
                        Please enter the amount you wish to sell in asset terms, not GBP.
                        The total payment you will receive will be displayed in GBP.
                        After confirming, you can send the asset to the chosen contact.
                    </p>
                </div>
                : null}
            <form onSubmit={sellAction} className="sell-form">
                <div className="help-tutorial">
                    <button type="button" className="tutorial-button" onClick={() => setShowTutorial(!showTutorial)}>?</button>
                </div>
                <label htmlFor="" className="main-label">Sell Crypto</label>
                <label htmlFor="amount" id="sellLabel">Crypto Assets</label>
                <input type="number" min="0.00001" step="0.000001" onChange={(e) => setAmountToSell(e.target.value)} name="amount" id="buy-amount" placeholder="Enter Amount" className="sellingInput" />
                <div className="information">
                    <p>Total Owned: {wallet?.balance}</p>
                    <p>Rate: 1 {wallet?.coin_symbol} = £{rate}</p>
                </div>
                <label htmlFor="receive-amount" id="receive-label">You will Receive</label>
                <div id="receive-amount">
                    <p>£{typeof Number(rate) === 'number' && amountToSell ? (Number(rate) * parseFloat(amountToSell)).toFixed(2) : '0.00'}</p>
                </div>
                <div className="buttons">
                    <button type="button" className="goBack" onClick={() => navigate(-1)}>Cancel</button>
                    <button type="submit" className="send-button">Sell</button>
                </div>
            </form>
        </div>
    );
};

export default SellCrypto;