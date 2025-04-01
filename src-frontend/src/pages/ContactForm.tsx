import { useState } from 'react';
import '../styles/ContactForm.css';
import api from '../lib/api';


export const ContactForm = ({goToList} : {goToList: () => void}) => {
    const [contactName, setContactName] = useState("");
    const [contactAddress, setContactAddress] = useState("");
    const [confirmMessage, setConfirmMessage] = useState("");
    const [isLoading, setIsLoading] = useState(false);

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

          // Check if the contact already exists
          const existingContacts = await api.getContacts();
          const nameExists = existingContacts.some(
              contact => contact.name.toLowerCase() === contactName.trim().toLowerCase()
          );
          const addressExists = existingContacts.some(
              contact => contact.address.toLowerCase() === contactAddress.trim().toLowerCase()
          );
          if (addressExists && nameExists || addressExists || nameExists) {
              setConfirmMessage("A contact with this address and/or name already exists - Both must be unique");
              return;
          }
          
          setIsLoading(true);
            const response = await api.addContact(contactName, contactAddress);
            const data = await response.json();

            if (response.ok) {
              console.log("New contact added");
              setConfirmMessage("Contact added successfully!");
              // Clear form
              setContactName("");
              setContactAddress("");
              // Navigate back to list after delay
              setTimeout(() => {
                  goToList();
              }, 100);
          } else {
              setConfirmMessage(data.error || "Failed to add contact");
          }
          // onRegister();
        } catch (err) {
          setConfirmMessage("Failed to add contact.");
          console.error(err);
        } finally {
          setIsLoading(false);
        }
      };


    return(
      <form onSubmit={handleAddContact} className="contact-form">
      <label htmlFor="" className="main-label">New Contact</label>
      <label htmlFor="contact" id="contactLabel">Contact Name</label>
      <input 
          type="text" 
          value={contactName}
          onChange={(e) => setContactName(e.target.value)} 
          name="contact" 
          id="contact" 
          placeholder="Enter name" 
          className="contactInput"
      />
      <label htmlFor="waddress" id="addresslabel">Enter Address</label>
      <input 
          type="text" 
          value={contactAddress}
          onChange={(e) => setContactAddress(e.target.value)} 
          name="waddress" 
          id="waddress" 
          placeholder="Enter wallet address" 
          className="contactInput"
      />
      <div className="buttons">
          <button type="button" className="goBack" onClick={goToList}>Cancel</button>
          <button 
              type="submit" 
              className="add-contact-button"
              disabled={isLoading}
          >
              {isLoading ? 'Adding...' : 'Add'}
          </button>
      </div>
      {confirmMessage && <p className={confirmMessage.includes("success") ? "success-message" : "error-message"}>{confirmMessage}</p>}
  </form>
    )
}


export default ContactForm;