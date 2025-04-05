import '../styles/SendCrypto.css';
import React, { useState, useEffect } from 'react';
import { useNavigate, useLocation } from "react-router-dom";
import { useToast } from '../contexts/ToastContext';
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
  //const [selectedOption, setSelectedOption] = useState("");
  const wallet = location.state?.wallet as Wallet;
  const [amountToSend, setAmountToSend] = useState("");
  //const [confirmMessage, setConfirmMessage] = useState("");
  const [newContact, setNewContact] = useState(false);
  const [existingContactsList, setExistingContactsList] = useState(false);
  //const [qrCodeContact, setQrCodeContact] = useState(false);
  const [contactChosen, setContactChosen] = useState("");
  const [activeButton, setActiveButton] = useState<string | null>(null);
  const [contacts, setContacts] = useState<Contact[]>([]);
  //const [loading, setLoading] = useState<boolean>(true);
  //const [error, setError] = useState<string>("");
  const { showToast } = useToast();
  const savedTheme = localStorage.getItem('theme');
  const [showTutorial, setShowTutorial] = useState<boolean>(false);

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
      //setLoading(true);
      const contactsList = await api.getContacts();
      setContacts(contactsList);
    } catch (err) {
      console.error("Error fetching contacts:", err);
      //setError("Failed to load contacts");
    } finally {
      //setLoading(false);
    }
  };



  //const handleChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
  //    setSelectedOption(event.target.value);
  //};

  const handleChangeContact = (event: React.ChangeEvent<HTMLSelectElement>) => {
    setContactChosen(event.target.value);
  };

  const sellAction = async (e: React.FormEvent) => {
    e.preventDefault();
    
    {/*}
    if (!selectedOption) {
        setConfirmMessage("Please select a cryptocurrency to send.");
        showToast("Please select a cryptocurrency to send.", "error");
        return;
    }*/}

    if (!amountToSend.trim() || parseFloat(amountToSend) <= 0) {
        //setConfirmMessage("Please enter a valid amount greater than 0.00001.");
        showToast("Please enter a valid amount greater than 0.00001.", "error");
        return;
    }

    if (!contactChosen){
        //setConfirmMessage("Please select a contact.");
        showToast("Please select a contact.", "error");
        return;
    }

    try {
        console.log("Crypto sending initiated.");
        //setConfirmMessage("Sent successful!");
        showToast("Sent successful!", "success");
        // Implement the actual purchase logic here
    } catch (err) {
        //setConfirmMessage("Transaction failed. Please try again.");
        showToast("Transaction failed. Please try again.", "error");
        console.error(err);
    }
  };

  const showNewContact = () => {
    setNewContact(true);
    setExistingContactsList(false);
    //setQrCodeContact(false);
    setActiveButton('new'); // Set active button to 'new'
  }

  const showExistingContacts = () => {
    setExistingContactsList(true);
    setNewContact(false);
    //setQrCodeContact(false);
    setActiveButton('existing'); // Set active button to 'existing'
  }

  {/*
  const showQrCodeScan = () => {
    setQrCodeContact(true);
    setNewContact(false);
    setExistingContactsList(false);
    setActiveButton('qrCode'); // Set active button to 'qrCode'
  }*/}


  return (
    <div className="return-container">
      {showTutorial?
        <div className="instructionBox">
          <button className="close-button" onClick={() => setShowTutorial(!showTutorial)}>
              ×
          </button>
          <p>Send Crypto allows you to send a quantity of your asset to another user's wallet.
            Please enter the amount you wish to send in asset terms, not GBP.
            Then choose a contact in which you would like to send it to. You may wish to choose from
            an existing contact or create a contact in the spot.
            After confirming, you can send the asset to the chosen contact.
          </p>
        </div>
      : null}
      <form onSubmit={sellAction} className="send-form">
        <div className="help-tutorial">
          <button type="button" className="tutorial-button" onClick={() => setShowTutorial(!showTutorial)}>?</button>
        </div>
        <label htmlFor="" className="main-label">Send Crypto</label>
        <label htmlFor="amount" id="sendLabel">Crypto Assets</label>
        <input type="number" min="0.00001" step="0.000001" onChange={(e) => setAmountToSend(e.target.value)} name="amount" id="buy-amount" placeholder="Enter Amount" className="sendingInput"/>
        <div className="information">
          <p>Total Owned: {wallet?.balance}</p>
        </div>
        <label htmlFor="contact-options" id="contacts">Choose Contact</label>
        <div id="contact-options">
          <button type="button" onClick={showNewContact} className={`contact-option-button ${activeButton === 'new' ? 'active' : ''}`}>New</button>
          <button type="button" onClick={showExistingContacts} className={`contact-option-button ${activeButton === 'existing' ? 'active' : ''}`}>Existing</button>
          {/*<button type="button" onClick={showQrCodeScan} className={`contact-option-button ${activeButton === 'qrCode' ? 'active' : ''}`}>QR code</button>*/}
        </div>
        {newContact? "display new contact form here (to be added)": null}
        {existingContactsList ? 
          <select id="existing-contacts-dropdown" value={contactChosen} onChange={handleChangeContact}>
            <option value="">--Choose an option--</option>
            {contacts.map((contact,index) => (
              <option key={index} value={contact.name}>{contact.name}</option>
            ))}
          </select>
          : (
          null
        )}
        {/*{qrCodeContact? "display QR code scanner here (to be added)": null}*/}
        <p className="label-contact-selection">Contact selected: {contactChosen}</p>
        <div className="buttons">
          <button type="button" className="goBack" onClick={() => navigate(-1)}>Cancel</button>
          <button type="submit" className="send-button">Sell</button>
        </div>
        {/*{confirmMessage && <p className="error-message">{confirmMessage}</p>}*/}
      </form>
    </div>
  );
};

export default SendCrypto;