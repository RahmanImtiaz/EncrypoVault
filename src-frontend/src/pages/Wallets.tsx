import React, { useState, useEffect } from 'react';
import '../styles/Wallets.css';

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

const Wallets: React.FC = () => {
  const [wallets, setWallets] = useState<Wallet[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  // Removed unused error state
  const [isVisible, setIsVisible] = useState<boolean>(false);
  const [newWalletName, setNewWalletName] = useState<string>("");
  
  useEffect(() => {
    fetchWallets();
  }, []);
  
  const fetchWallets = async () => {
    try {
      setLoading(true);
      const wallets = await window.api.get_portfolio_wallets();
      setWallets(wallets);
    } catch (err) {
      console.error('Error fetching wallets:', err);
      console.error('Failed to load wallets');
    } finally {
      setLoading(false);
    }
  };
  
  const toggleForm = () => setIsVisible(!isVisible);
  
  const createNewWallet = async (event: React.FormEvent) => {
    event.preventDefault();
    if (!newWalletName.trim()) {
      alert('Please enter a wallet name');
      return;
    }
    
    try {
      // Add API call to create wallet here
      // await window.api.create_wallet(newWalletName);
      alert(`New wallet "${newWalletName}" created`);
      setNewWalletName("");
      toggleForm();
      // Refresh wallet list
      fetchWallets();
    } catch (err) {
      console.error('Error creating wallet:', err);
      alert('Failed to create wallet');
    }
  };

  if (loading) {
    return <div className="walletContaiter"><p>Loading wallets...</p></div>;
  }

  return (
    <div className="walletContainer">
      <div className="walletHeading">
        <h1>Your Wallets</h1>
        <button onClick={toggleForm}>Add Wallet</button>
      </div>
      
      {isVisible && (
        <form onSubmit={createNewWallet} className='walletForm'>
          <label htmlFor="walletName" className="formLabel">Create new wallet:</label>
          <div className="inputArea">
            <input 
              type="text" 
              id="walletName"
              placeholder='Enter name' 
              className="inputWallet"
              value={newWalletName}
              onChange={(e) => setNewWalletName(e.target.value)}
            />
            <button type="submit" className="add-wallet-button">Create</button>
            <button type="button" onClick={toggleForm} className="goBack">Cancel</button>
          </div>
        </form>
      )}
      
      {wallets.length === 0 ? (
        <p className="message">No wallets found. Create a wallet to get started.</p>
      ) : (
        <div className="walletList">
          {wallets.map((wallet, index) => (
            <div key={index} className="walletItem">
              <div className="walletItemHeader">
                <h3>{wallet.name}</h3>
                <span className="walletBalance">£{wallet.balance.toFixed(2)}</span>
              </div>
              <p className="walletAddress">Address: {wallet.address}</p>
              <p className="walletType">Type: {wallet.coin_symbol}</p>
              
              {Object.keys(wallet.holdings).length > 0 && (
                <div className="holdingsSection">
                  <h4>Holdings</h4>
                  {Object.entries(wallet.holdings).map(([cryptoId, holding]) => (
                    <div key={cryptoId} className="holdingItem">
                      <span>{holding.name} ({holding.symbol.toUpperCase()})</span>
                      <span>{holding.amount.toFixed(8)}</span>
                      <span>£{holding.value.toFixed(2)}</span>
                    </div>
                  ))}
                </div>
              )}
              
              <div className="walletActions">
                <button className="walletAction">Send</button>
                <button className="walletAction">Receive</button>
                <button className="walletAction">Trade</button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default Wallets;