// Portfolio.tsx
import React from 'react';
import { useState } from 'react';
import '../styles/Wallets.css';




const Wallets: React.FC = () => {
  const [isVisible, setIsVisible] = useState(false);
  const toggleForm = () => setIsVisible(!isVisible);
  const createNewWallet = (event: React.FormEvent) =>{
    event.preventDefault();
    console.log('new wallet created');
    return alert('new wallet created');
  }


  return (
    <div className="walletContaiter">
      <div className="walletHeading">
        <h1>Wallet</h1>
        <button onClick={toggleForm}>add wallet</button>
      </div>
      {isVisible && (
        <form onSubmit={createNewWallet} className='walletForm'>
          <label htmlFor="" className="formLabel">Create new wallet:</label>
          <div className="inputArea">
          <input type="text" placeholder='Enter name' className="inputWallet"/>
          <button type="submit" className="add-wallet-button">Create</button>
          <button type="button" onClick={toggleForm} className="goBack">Cancel</button>
          </div>
        </form>
      )}
      <div className="walletList">
          <div>Wallet1</div>
          <div>Wallet2</div>
          <div>Wallet3</div>
      </div>
    </div>
  );
};

export default Wallets;