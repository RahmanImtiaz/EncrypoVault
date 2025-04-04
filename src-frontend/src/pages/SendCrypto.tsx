import '../styles/SendCrypto.css';
import React, { useState } from 'react';
import { useNavigate } from "react-router-dom";
import { useToast } from '../contexts/ToastContext';

const SendCrypto = () => {
  const navigate = useNavigate();
  const [selectedOption, setSelectedOption] = useState("");
  const [amountToSend, setAmountToSend] = useState("");
  const [confirmMessage, setConfirmMessage] = useState("");
  const [newContact, setNewContact] = useState(false);
  const [existingContactsList, setExistingContactsList] = useState(false);
  const [qrCodeContact, setQrCodeContact] = useState(false);
  const [contactChosen, setContactChosen] = useState("");
  const [activeButton, setActiveButton] = useState<string | null>(null);
  const { showToast } = useToast();

  const handleChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
      setSelectedOption(event.target.value);
  };

  const handleChangeContact = (event: React.ChangeEvent<HTMLSelectElement>) => {
    setContactChosen(event.target.value);
  };

  const sellAction = async (e: React.FormEvent) => {
    e.preventDefault();
        
    if (!selectedOption) {
        setConfirmMessage("Please select a cryptocurrency to send.");
        showToast("Please select a cryptocurrency to send.", "error");
        return;
    }

    if (!amountToSend.trim() || parseFloat(amountToSend) <= 0) {
        setConfirmMessage("Please enter a valid amount greater than 0.00001.");
        showToast("Please enter a valid amount greater than 0.00001.", "error");
        return;
    }

    if (!contactChosen){
        setConfirmMessage("Please select a contact.");
        showToast("Please select a contact.", "error");
        return;
    }

    try {
        console.log("Crypto sending initiated.");
        setConfirmMessage("Sent successful!");
        showToast("Sent successful!", "success");
        // Implement the actual purchase logic here
    } catch (err) {
        setConfirmMessage("Transaction failed. Please try again.");
        showToast("Transaction failed. Please try again.", "error");
        console.error(err);
    }
  };

  const showNewContact = () => {
    setNewContact(true);
    setExistingContactsList(false);
    setQrCodeContact(false);
    setActiveButton('new'); // Set active button to 'new'
  }

  const showExistingContacts = () => {
    setExistingContactsList(true);
    setNewContact(false);
    setQrCodeContact(false);
    setActiveButton('existing'); // Set active button to 'existing'
  }

  const showQrCodeScan = () => {
    setQrCodeContact(true);
    setNewContact(false);
    setExistingContactsList(false);
    setActiveButton('qrCode'); // Set active button to 'qrCode'
  }

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
                <input type="text" min="0.00001" step="0.000001" onChange={(e) => setAmountToSend(e.target.value)} name="amount" id="amount" placeholder="Enter Amount" className="sellingInput"/>
            </div>
            <div className="information">
                <p>Total Owned: ...</p>
                <p>Rate: 1 {selectedOption} = "£..."</p>
            </div>
            <label htmlFor="contact-options" id="contacts">Choose Contact</label>
            <div id="contact-options">
                <button type="button" onClick={showNewContact} className={`contact-option-button ${activeButton === 'new' ? 'active' : ''}`}>New</button>
                <button type="button" onClick={showExistingContacts} className={`contact-option-button ${activeButton === 'existing' ? 'active' : ''}`}>Existing</button>
                <button type="button" onClick={showQrCodeScan} className={`contact-option-button ${activeButton === 'qrCode' ? 'active' : ''}`}>QR code</button>
            </div>
            {newContact? "display new contact form here (to be added)": null}
            {existingContactsList ? 
                <select id="existing-contacts-dropdown" value={contactChosen} onChange={handleChangeContact}>
                    <option value="">--Choose an option--</option>
                    <option value="Steve">Steve</option>
                    <option value="Lisa">Lisa</option>
                    <option value="Fake 3">Fake 3</option>
                    <option value="Fake 4">Fake 4</option>
                </select>
            : null}
            {qrCodeContact? "display QR code scanner here (to be added)": null}
            <p className="label-contact-selection">Contact selected: {contactChosen}</p>
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