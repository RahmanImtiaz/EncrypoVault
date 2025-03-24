// Portfolio.tsx
//import React from 'react';
//import '../styles/ContactList.css';
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






const ContactList = ({goToForm} : {goToForm: () => void}) => {
  return (
    <div className="contactsListContainer">
      <div className="contactsListHeading">
        <h1>Contacts</h1>
        <button onClick={goToForm}>add contact</button>
      </div>
      <div className="contactsList-list">
        <p>No contacts added yet</p>
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