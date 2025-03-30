import { useState } from 'react';
import '../styles/ContactForm.css';


export const ContactForm = ({goToList} : {goToList: () => void}) => {
    const [contactName, setContactName] = useState("");
    const [contactAddress, setContactAddress] = useState("");
    const [confirmMessage, setConfirmMessage] = useState("");

    const handleAddContact = async (e: React.FormEvent) => {
        e.preventDefault();
        
        if (!contactName.trim()) {
            setConfirmMessage("Please enter contact name");
            return;
        }
        
        if (!contactAddress.trim()) {
            setConfirmMessage("Please enter an address");
            return;
        }
    
        try {
          // Check if the account already exists
          //const accounts = await window.pywebview.api.get_accounts();
          //if (accounts.includes(accountName)) {
            //  setError("Account already exists. Please choose a different account name.");
            //  return;
          //}
          // Here you would call your backend to register the account
          //const response = await window.pywebview.api.create_account(accountName, password, accountType)
          //console.log(response)
          console.log("New contact added");
          setConfirmMessage("New contact added");
          // onRegister();
        } catch (err) {
            setConfirmMessage("Failed to add contact.");
          console.error(err);
        }
      };


    return(
        <form onSubmit={handleAddContact} className="contact-form">
            <label htmlFor="" className="main-label">New Contact</label>
            <label htmlFor="contact" id="contactLabel">Contact Name</label>
            <input type="text" onChange={(e) => setContactName(e.target.value)} name="contact" id="contact" placeholder="Enter name" className="contactInput"/>
            <label htmlFor="waddress" id="addresslabel">Enter Address</label>
            <input type="text" onChange={(e) => setContactAddress(e.target.value)} name="waddress" id="waddress" placeholder="Enter wallet address" className="contactInput"/>
            <button type="button" className="qrcode">Scan QR code</button>
            <div className="buttons">
                <button type="button" className="goBack" onClick={goToList}>Cancel</button>
                <button type="submit" className="add-contact-button">Add</button>
            </div>
            {confirmMessage && <p className="error-message">{confirmMessage}</p>}
        </form>
    )
}


export default ContactForm;