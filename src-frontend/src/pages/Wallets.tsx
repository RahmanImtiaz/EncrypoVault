import React, { useState, useEffect } from 'react';
import '../styles/Wallets.css';
import fetchPrice from '../components/fetchPrice';
import { useToast } from '../contexts/ToastContext';
import { useNavigate } from 'react-router-dom';

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
  const {priceData} = fetchPrice();
  const [copiedAddresses, setCopiedAddresses] = useState<{[key: string]: boolean}>({});
  const { showToast } = useToast();
  const [selectedWallet, setSelectedWallet] = useState<Wallet | null>(null);  
  const navigate = useNavigate();
  const savedTheme = localStorage.getItem('theme');

  useEffect(() => {
    if (savedTheme === 'light')
      document.body.classList.add('light-mode');
    else 
      document.body.classList.remove('light-mode');
  }, [savedTheme]);


  useEffect(() => {
    fetchWallets();
  }, []);


  const handleWalletClick = (wallet: Wallet) => {
    setSelectedWallet(wallet);
    console.log('Selected wallet:', wallet);
    navigate('/WalletInfo', { state: { wallet } });
  }

  useEffect(() => {
    if (selectedWallet) {
      console.log('Selected wallet:', selectedWallet);
    }
  }
  , [selectedWallet]);
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

  const copyToClipboard = (text: string, walletIndex: number) => {
    navigator.clipboard.writeText(text).then(() => {
      // Set copied state for this specific wallet
      setCopiedAddresses(prev => ({...prev, [walletIndex]: true}));
      
      // Reset copied state after 2 seconds
      setTimeout(() => {
        setCopiedAddresses(prev => ({...prev, [walletIndex]: false}));
      }, 2000);
    }).catch(err => {
      console.error('Failed to copy address:', err);
    });
  };

  const fetchWallets = async () => {
    try {
      setLoading(true);
      const wallets = await window.api.getWallets();
      console.log('Fetched wallets:', wallets);
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
      showToast('Please enter a wallet name', 'error');
      return;
    }

    // Check if wallet name contains at least one letter - bitcoinlib requires it
    if (!/[a-zA-Z]/.test(newWalletName)) {
      showToast('Wallet name must contain at least one letter character', 'error');
      return;
    }

    try {
      // Add API call to create wallet here
      const response = await window.api.createWallet(newWalletName);
      if (response.ok) {
        const walletData = await response.json();

        // Transform the API response to match the expected wallet interface
        const newWallet: Wallet = {
          name: walletData.walletName || newWalletName,
          address: walletData.walletAddress || "",
          balance: 0,  // Initialize with zero balance
          coin_symbol: walletData.walletType || "BTC",
          holdings: {}  // Initialize with empty holdings
        };
        //await fetchWallets();
        setWallets([...wallets, newWallet]);
        setFilteredWallets([...filteredWallets, newWallet]);
        setNewWalletName("");
        showToast(`New wallet "${newWalletName}" created`, 'success');
        setIsCreatingWallet(false);
      } else {
        showToast('Failed to create wallet', 'error');
      }

    } catch (err) {
      console.error('Error creating wallet:', err);
      showToast('Failed to create wallet', 'error');
    }
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
                <span className="wallet-balance">
                  {(() => {
                  const priceKey = wallet.coin_symbol === "BTC" ? "BTC-GBP" : "ETH-GBP";
                  const price = priceData?.[priceKey];
                  
                  if (price !== undefined) {
                    return `£${(wallet.balance * Number(price)).toFixed(2)}`;
                  } else {
                    return `£${wallet.balance.toFixed(2)}`;
                  }
                  })()}
                </span>
              </div>
              <div className="wallet-content">
                <div className="wallet-details">
                  <div className="wallet-detail-row">
                    <span className="wallet-detail-label">Address:</span>
                    <span className="wallet-detail-value">{wallet.address.substring(0, 20)}...</span>
                    <button
                      className={`copy-btn ${copiedAddresses[index] ? 'copied' : ''}`}
                      onClick={(e) => {
                        e.stopPropagation();
                        copyToClipboard(wallet.address, index);
                      }}
                      title="Copy address"
                    >
                      {copiedAddresses[index] ? (
                        <>
                          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                            <polyline points="20 6 9 17 4 12"></polyline>
                          </svg>
                          <span>Copied!</span>
                        </>
                      ) : (
                        <>
                          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                            <rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect>
                            <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1-2 2v1"></path>
                          </svg>
                          <span>Copy</span>
                        </>
                      )}
                    </button>
                  </div>
                  <div className="wallet-detail-row">
                    <span className="wallet-detail-label">Type:</span>
                    <span className="wallet-detail-value">{wallet.coin_symbol}</span>
                  </div>
                  <div className="wallet-detail-row">
                    <span className="wallet-detail-label">Holdings:</span>
                    <span className="wallet-detail-value">
                        {wallet.balance} {wallet.coin_symbol}
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
