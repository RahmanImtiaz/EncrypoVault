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
  const [filteredWallets, setFilteredWallets] = useState<Wallet[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [isCreatingWallet, setIsCreatingWallet] = useState<boolean>(false);
  const [newWalletName, setNewWalletName] = useState<string>("");
  const [searchQuery, setSearchQuery] = useState<string>("");
  
  useEffect(() => {
    fetchWallets();
  }, []);
  
  useEffect(() => {
    // Filter wallets based on search query
    if (searchQuery.trim() === '') {
      setFilteredWallets(wallets);
    } else {
      const filtered = wallets.filter(wallet => 
        wallet.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
        wallet.coin_symbol.toLowerCase().includes(searchQuery.toLowerCase())
      );
      setFilteredWallets(filtered);
    }
  }, [searchQuery, wallets]);
  
  const fetchWallets = async () => {
    try {
      setLoading(true);
      const wallets = await window.api.getPortfolioWallets();
      setWallets(wallets);
      setFilteredWallets(wallets);
    } catch (err) {
      console.error('Error fetching wallets:', err);
    } finally {
      setLoading(false);
    }
  };
  
  const toggleCreateForm = () => {
    setIsCreatingWallet(!isCreatingWallet);
    setNewWalletName("");
  };
  
  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    // Search is already handled by the useEffect
  };
  
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
      setIsCreatingWallet(false);
      fetchWallets(); // Refresh wallet list
    } catch (err) {
      console.error('Error creating wallet:', err);
      alert('Failed to create wallet');
    }
  };

  const handleWalletClick = (wallet: Wallet) => {
    // Go to wallet details page
    console.log(`Navigating to wallet: ${wallet.name}`);
    // its empty for now
  };

  if (loading) {
    return (
      <div className="wallets-container">
        <div className="loading-state">
          <div className="loading-spinner"></div>
        </div>
      </div>
    );
  }

  return (
    <div className="wallets-container">
      <div className="wallets-header">
        <h1 className="wallets-title">Your Wallets</h1>
        <button className="add-wallet-btn" onClick={toggleCreateForm}>
          + Add New Wallet
        </button>
      </div>
      
      <div className="wallets-toolbar">
        {isCreatingWallet ? (
          <form onSubmit={createNewWallet} className="create-form">
            <span className="create-label">Create new wallet:</span>
            <input 
              type="text" 
              className="create-input"
              placeholder="Enter wallet name"
              value={newWalletName}
              onChange={(e) => setNewWalletName(e.target.value)}
              autoFocus
            />
            <button type="submit" className="create-btn">Create</button>
            <button type="button" className="cancel-btn" onClick={toggleCreateForm}>Cancel</button>
          </form>
        ) : (
          <form onSubmit={handleSearch} className="search-form">
            <input 
              type="text" 
              className="search-input"
              placeholder="Search wallets by name or type..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
            />
            <button type="submit" className="search-btn">Search</button>
          </form>
        )}
      </div>
      
      {filteredWallets.length === 0 ? (
        <div className="empty-state">
          <p>No wallets found. Create a wallet to get started.</p>
          <button className="add-wallet-btn" onClick={toggleCreateForm}>
            + Create Wallet
          </button>
        </div>
      ) : (
        <div className="wallets-list">
          {filteredWallets.map((wallet, index) => (
            <div 
              key={index} 
              className="wallet-item" 
              onClick={() => handleWalletClick(wallet)}
            >
              <div className="wallet-header">
                <h3 className="wallet-name">{wallet.name}</h3>
                <span className="wallet-balance">£{wallet.balance.toFixed(2)}</span>
              </div>
              <div className="wallet-content">
                <div className="wallet-details">
                  <div className="wallet-detail-row">
                    <span className="wallet-detail-label">Address:</span>
                    <span className="wallet-detail-value">{wallet.address.substring(0, 20)}...</span>
                  </div>
                  <div className="wallet-detail-row">
                    <span className="wallet-detail-label">Type:</span>
                    <span className="wallet-detail-value">{wallet.coin_symbol}</span>
                  </div>
                  <div className="wallet-detail-row">
                    <span className="wallet-detail-label">Holdings:</span>
                    <span className="wallet-detail-value">
                      {Object.keys(wallet.holdings).length} assets
                    </span>
                  </div>
                </div>
                
                <button className="wallet-view-btn" title="View wallet details">
                  →
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default Wallets;
