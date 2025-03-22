// Portfolio.tsx
import React from 'react';
import '../styles/Contacts.css';

const Contacts: React.FC = () => {
  return (
    <div className="contactsContainer">
      <div className="contactsHeading">
        <h1>Contacts</h1>
        <button>add contact</button>
      </div>
      <div className="contactsList">
        <p>No contacts added yet</p>
      </div>
    </div>
  );
};

export default Contacts;