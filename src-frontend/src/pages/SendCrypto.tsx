import '../styles/SendCrypto.css';
import React, { useState, useEffect } from 'react';
import { useNavigate, useLocation } from "react-router-dom";
import { useToast } from '../contexts/ToastContext';
import api from '../lib/api';
//import { PublicKeyCredentialRequestOptionsJSON, startAuthentication } from '@simplewebauthn/browser';
import { getWalletBalance } from '../components/helpers/FakeTransactionRecords';

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

interface Contact {
  name: string;
  address: string;
}


const SendCrypto = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const wallet = location.state?.wallet as Wallet;
  const [amountToSend, setAmountToSend] = useState("");
  const [contactChosen, setContactChosen] = useState("");
  const [contacts, setContacts] = useState<Contact[]>([]);
  const { showToast } = useToast();
  const savedTheme = localStorage.getItem('theme');
  const [showTutorial, setShowTutorial] = useState<boolean>(false);
  const [detailsScreen, showDetailsScreen] = useState(false);

  useEffect(() => {
    if (savedTheme === 'light')
      document.body.classList.add('light-mode');
    else
      document.body.classList.remove('light-mode');
  }, [savedTheme]);

  useEffect(() => {
    fetchContacts();
  }, []);

  const fetchContacts = async () => {
    try {
      const contactsList = await api.getContacts();
      setContacts(contactsList);
    } catch (err) {
      console.error("Error fetching contacts:", err);
    }
  };


  const handleChangeContact = (event: React.ChangeEvent<HTMLSelectElement>) => {
    setContactChosen(event.target.value);
  };

  const sellAction = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!amountToSend.trim() || parseFloat(amountToSend) <= 0) {
      showToast("Please enter a valid amount greater than or equal to 0.00001.", "error");
      return;
    }

    {/*}
    if (parseFloat(amountToSend) > wallet.balance) {
        showToast("Insufficient balance. Please enter a valid amount up to or equal to your balance.", "error");
        return;
    }*/}

    if (!contactChosen) {
      showToast("Please select a contact.", "error");
      return;
    }

    showDetailsScreen(true);

  };



  const sendConfirm = async () => {
    try {
      // Trigger biometric verification
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
        // const authData: PublicKeyCredentialRequestOptionsJSON = await window.api.getWebauthnLoginOpts() as unknown as PublicKeyCredentialRequestOptionsJSON
        // const webauthnResponse = await startAuthentication({ optionsJSON: authData, useBrowserAutofill: false })
        const response = await api.verifyBiometricForTransaction(wallet);

        if (response.status !== 200) {
          showToast('Invalid Password or biometrics!', 'error');
          return;
        }
      }

      // Find the selected contact's address
      const selectedContact = contacts.find(contact => contact.name === contactChosen);

      if (!selectedContact) {
        showToast("Contact not found.", "error");
        return;
      }

      // Send the crypto using the wallet name, amount, and destination address
      await api.sendCrypto(wallet.name, parseFloat(amountToSend), selectedContact.address);

      console.log("Crypto sending initiated.");
      showToast("Sent successful!", "success");

      // Go back to previous page after successful transaction
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
            <p>Amount to send: {amountToSend} {wallet?.coin_symbol}</p>
            <p>Contact selected: {contactChosen}</p>
          </div>
          <div className="confirmation-buttons">
            <button type="button" className="cancel-confirmation" onClick={() => showDetailsScreen(false)}>Cancel</button>
            <button type="button" className="confirm-transaction-button" onClick={() => sendConfirm()}>Confirm</button>
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
          <p>Send Crypto allows you to send a quantity of your asset to another user's wallet.
            Please enter the amount you wish to send in asset terms, not GBP.
            Then choose a contact in which you would like to send it to from the list of existing contacts.
          </p>
          <p>If no contacts are available, please add a new contact in the contacts page.
            After confirming, you can send the asset to the chosen contact.</p>
        </div>
        : null}
      <form onSubmit={sellAction} className="send-form">
        <div className="help-tutorial">
          <button type="button" className="tutorial-button" onClick={() => setShowTutorial(!showTutorial)}>?</button>
        </div>
        <label htmlFor="" className="main-label">Send Crypto</label>
        <label htmlFor="amount" id="sendLabel">Crypto Assets</label>
        <input type="number" min="0.00001" step="0.000001" onChange={(e) => setAmountToSend(e.target.value)} name="amount" id="buy-amount" placeholder="Enter Amount" className="sendingInput" />
        <div className="information">
          <p>Total Owned: {getWalletBalance(wallet)} {wallet?.coin_symbol}</p>
        </div>
        <label htmlFor="contact-options" id="contacts">Choose Contact</label>
        <select id="existing-contacts-dropdown" value={contactChosen} onChange={handleChangeContact}>
          <option value="">--Choose an option--</option>
          {contacts.map((contact, index) => (
            <option key={index} value={contact.name}>{contact.name}</option>
          ))}
        </select>
        <p className="label-contact-selection">Contact selected: {contactChosen}</p>
        <div className="buttons">
          <button type="button" className="goBack" onClick={() => navigate(-1)}>Cancel</button>
          <button type="submit" className="send-button">Send</button>
        </div>
      </form>
    </div>
  );
};

export default SendCrypto;