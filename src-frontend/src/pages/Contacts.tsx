//import React from 'react';
/*import '../styles/Contacts.css';*/
import { useState } from 'react';


//import { Contact } from "./types";
import ContactList from './ContactList';
import ContactForm from './ContactForm';


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
/*
const Contacts = () => {
  return (
    <div className="contactsContainer">
      <div className="contactsHeading">
        <h1>Contacts</h1>
        <button onClick={toggleContacts}>add contact</button>
      </div>
      <div className="contactsList">
        <p>No contacts added yet</p>
      </div>
    </div>
  );
};*/


export const Contacts = () => {
  const [inContactsListPage, setInContactsListPage] = useState(true);

  return (
    <div>
      {inContactsListPage ?
      (<ContactList goToForm = {() => setInContactsListPage(false)}/>) 
      : (<ContactForm goToList = {() => setInContactsListPage(true)}/>)}
    </div>
  );
}

export default Contacts;








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