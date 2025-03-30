// Portfolio.tsx
//import React from 'react';
import { useState, useEffect } from 'react';
import '../styles/ContactList.css';
import api from '../lib/api';
//import { useState } from 'react';
//import { Contact } from "./types";


/*
interface ContactListProps{
  contacts: Contact[];
  onAddContact: () => void;
}*/
/*
const [isContactDisplay, setIsContactDisplay] = useState(true);


const toggleContacts = () => {
  setIsContactDisplay(!isContactDisplay);
  console.log(isContactDisplay);
};*/

//for later:
//const Contacts = ({contacts, onAddContact} : ContactListProps) => {

//calls the function when button is clicked.
//<button onClick={toggleContacts}>add contact</button>

interface Contact {
  name: string;
  address: string;
}

const ContactList = ({goToForm} : {goToForm: () => void}) => {
  const [contacts, setContacts] = useState<Contact[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string>("");

  useEffect(() => {
    fetchContacts();
  }, []);
  
  const fetchContacts = async () => {
    try {
      setLoading(true);
      const contactsList = await api.getContacts();
      setContacts(contactsList);
    } catch (err) {
      console.error("Error fetching contacts:", err);
      setError("Failed to load contacts");
    } finally {
      setLoading(false);
    }
  };


  return (
    <div className="contactsListContainer">
      <div className="contactsListHeading">
        <h1>Contacts</h1>
        <button onClick={goToForm}>add contact</button>
      </div>
      <div className="contactsList-list">
        {loading ? (
          <div className="loading-spinner"></div>
        ) : error ? (
          <p className="error-message">{error}</p>
        ) : contacts.length > 0 ? (
          <ul className="contacts-list">
            {contacts.map((contact, index) => (
              <li key={index} className="contact-item">
                <div className="contact-name">{contact.name}</div>
                <div className="contact-address">{contact.address}</div>
              </li>
            ))}
          </ul>
        ) : (
          <p>No contacts added yet</p>
        )}
      </div>
    </div>
  );
};

export default ContactList;








/*to be used later





import { Contact } from "./types";

interface ContactListProps {
  contacts: Contact[];
  onAddContact: () => void;
}

const Contacts = ({ contacts, onAddContact }: ContactListProps) => {
  return (
    <div className="p-4">
      <h1 className="text-xl font-bold mb-4">Contacts</h1>
      <ul className="mb-4">
        {contacts.length > 0 ? (
          contacts.map((contact, index) => (
            <li key={index} className="p-2 border-b">{contact.name} - {contact.address}</li>
          ))
        ) : (
          <p>No contacts available.</p>
        )}
      </ul>
      <button onClick={onAddContact} className="bg-green-500 text-white p-2 rounded-md">
        Add Contact
      </button>
    </div>
  );
};

export default Contacts;


*/