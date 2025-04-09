import { useLocation } from 'react-router-dom';
import { useNavigate } from "react-router-dom";
import { useEffect, useState } from 'react';
import { QRCodeComponent } from '../components/generateQR';
import fetchPrice from '../components/fetchPrice';
import '../styles/WalletInfo.css';
// import { getWalletBalance } from '../components/helpers/FakeTransactionRecords';
import api from '../lib/api';

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
  fake_balance: string;
  holdings: {
    [key: string]: Holding;
  };
}

interface Transaction {
  timestamp: string;
  amount: number;
  hash: string;
  sender: string;
  receiver: string;
  name: string;
  confirmed?: boolean
}

const WalletInfo = () => {
  const location = useLocation();
  const initialWallet = location.state?.wallet as Wallet;
  const [wallet, setWallet] = useState<Wallet | null>(initialWallet);
  const [showQR, setShowQR] = useState(false);
  const [showTxModal, setShowTxModal] = useState(false);
  const [selectedTx, setSelectedTx] = useState<Transaction | null>(null);
  const [loading, setLoading] = useState(false);
  const [transactions, setTransactions] = useState<Transaction[]>([]);
  const navigate = useNavigate();
  const { priceData } = fetchPrice();
  const savedTheme = localStorage.getItem('theme');

  const fetchConfirmationStatus = async (txid: string): Promise<boolean> => {
    try {
      const response = await fetch(`https://blockstream.info/testnet/api/tx/${txid}/status`);
      const data = await response.json();
      return data.confirmed;
    } catch (error) {
      console.error('Error fetching confirmation status:', error);
      return false; // Assume unconfirmed if there's an error
    }
  };
  

  // Function to fetch the latest wallet data
  const refreshWalletData = async () => {
    if (!initialWallet) return;

    setLoading(true);
    try {
      const wallets: Wallet[] = await api.getWallets();
      const updatedWallet = wallets.find((w: Wallet) => w.name === initialWallet.name);

      if (updatedWallet) {
        setWallet(updatedWallet);
      }

      const allTransactions = await api.getAllTransactions();
      // Filter transactions for this wallet
      const walletTransactions = allTransactions.filter(tx => tx.name === initialWallet.name);
      const transactionsWithStatus = await Promise.all(
        walletTransactions.map(async (tx) => {
          const isFake = tx.hash.startsWith('fake-');
          const confirmed = isFake ? true : await fetchConfirmationStatus(tx.hash);
          return { ...tx, confirmed };
        })
      );
      setTransactions(transactionsWithStatus);
    } catch (error) {
      console.error('Error refreshing wallet data:', error);
      setTransactions([]);
    } finally {
      setLoading(false);
    }
  };

  // Refresh on initial mount
  useEffect(() => {
    refreshWalletData();
  }, []);

  // Listen for navigation events to refresh data when returning to this page
  useEffect(() => {
    const handleVisibilityChange = () => {
      if (document.visibilityState === 'visible') {
        refreshWalletData();
      }
    };

    document.addEventListener('visibilitychange', handleVisibilityChange);

    return () => {
      document.removeEventListener('visibilitychange', handleVisibilityChange);
    };
  }, []);

  // Add a focus event listener to refresh when returning from other pages
  useEffect(() => {
    window.addEventListener('focus', refreshWalletData);
    return () => {
      window.removeEventListener('focus', refreshWalletData);
    };
  }, []);

  useEffect(() => {
    if (savedTheme === 'light')
      document.body.classList.add('light-mode');
    else
      document.body.classList.remove('light-mode');
  }, [savedTheme]);

  const handleTxClick = (tx: Transaction) => {
    setSelectedTx(tx);
    setShowTxModal(true);
  };

  if (!wallet) {
    return <div className="wallet-info-container">
      {loading ? "Loading wallet data..." : "No wallet selected"}
    </div>;
  }

  if (showQR) {
    return (
      <div className="qr-modal-overlay">
        <div className="qr-modal-content">
          <div className="modal-header">
            <h2>{wallet.name}</h2>
          </div>
          <QRCodeComponent
            value={wallet.address}
            size={256}
            level="Q"
            bgColor="#FFFFFF"
            fgColor="#000000"
          />
          <p className="address-text"> Wallet Address: {wallet.address}</p>
          <button
            className="close-button"
            onClick={() => setShowQR(false)}
          >
            ×
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className='info-container'>
      <div className='wallet-name'>
        <button className="previous-page" onClick={() => navigate(-1)}>←</button>
        <h2>{wallet.name} Details</h2>
        <button
          className="refresh-button"
          onClick={refreshWalletData}
          disabled={loading}
        >
          {loading ? "..." : "↻"}
        </button>
      </div>

      <div className='wallet-details'>
        <div className="wallet-balance">
          <h3 className='big'>Balance:
            {(() => {
              const priceKey = wallet.coin_symbol === "BTC" ? "BTC-GBP" : "ETH-GBP";
              const price = priceData?.[priceKey];
              const total = Number(wallet.balance) + Number(wallet.fake_balance);

              if (price !== undefined) {
                return `£${(total * Number(price)).toFixed(2)}`;
              } else {
                return `£${wallet.balance.toFixed(2)}`;
              }
            })()}
          </h3>
        </div>
        <div className='wallet-coin-symbol'>
          <h4 className='smaller'>Coin Symbol: {wallet.coin_symbol}</h4>
        </div>
        <div className='wallet-holdings'>
          <h3>Holdings:</h3>
          <p className="balance-display">
            {(Number(wallet.balance) + Number(wallet.fake_balance)).toFixed(8)} {wallet?.coin_symbol}
          </p>
        </div>
        <div className="buttons">
          <button className="wallet-button" onClick={() => navigate("/buy", { state: { wallet } })}>Buy {wallet.coin_symbol}</button>
          <button className="wallet-button" onClick={() => navigate("/sell", { state: { wallet } })}>Sell {wallet.coin_symbol}</button>
          <button className="wallet-button" onClick={() => navigate("/send", { state: { wallet } })}>Send {wallet.coin_symbol}</button>
          <button className="wallet-button" onClick={() => setShowQR(true)}>Receive {wallet.coin_symbol}</button>
        </div>
        <div className='wallet-address'>
          <h3>Address: {wallet.address}</h3>
        </div>
      </div>

      {/* Transaction History Section */}
<div className="transaction-history">
  <h3>Transaction History</h3>
  {transactions.length === 0 ? (
    <p className="no-transactions">No transactions yet</p>
  ) : (
    <div className="transactions-list">
      {transactions.map((tx) => {
        const isOutgoing = tx.sender === wallet.address;
        console.log(tx.sender)
        console.log(wallet.address)
        const isFakeBuy = tx.sender === "exchange";
        const isFakeSell = tx.receiver === "exchange";
        const isConfirmed = tx.confirmed ?? false; // All fake transactions are confirmed

        return (
          <div
            key={tx.hash}
            className={`transaction-item ${
              isOutgoing  ? 'out' : 'in'
            } ${
              isFakeBuy ? 'fake-buy' : isFakeSell ? 'fake-sell' : ''
            }`}
            onClick={() => handleTxClick(tx)}
          >
            <div className="tx-direction">
              {isOutgoing ? '⬆️' : '⬇️'}
            </div>
            <div className="tx-details">
              <div className="tx-amount">
                {isOutgoing ? '-' : '+'}{tx.amount} {wallet.coin_symbol}
                {(isFakeBuy || isFakeSell) && (
                  <span className="tx-type-badge">
                    {isFakeBuy ? 'BUY' : 'SELL'}
                  </span>
                )}
              </div>
              <div className="tx-time">
                {new Date(tx.timestamp).toLocaleString()}
              </div>
            </div>
            <div className={`tx-status ${isConfirmed ? 'confirmed' : 'pending'}`}>
              {isConfirmed ? 'confirmed' : 'pending'}
            </div>
            <div className="tx-id">
              {tx.hash.startsWith('fake-') 
                ? tx.hash.replace('fake-buy-', '').replace('fake-sell-', '').substring(0, 8)
                : tx.hash.substring(0, 12)}...
            </div>
          </div>
        );
      })}
    </div>
  )}
</div>

      {/* Transaction Details Modal */}
      {showTxModal && selectedTx && (
        <div className="tx-modal-overlay" onClick={() => setShowTxModal(false)}>
          <div className="tx-modal-content" onClick={(e) => e.stopPropagation()}>
            <button
              className="close-button"
              onClick={() => setShowTxModal(false)}
            >
              ×
            </button>

            <h3>Transaction Details</h3>
            <div className="tx-summary">
              <p><strong>TXID:</strong> {selectedTx.hash}</p>
              <p><strong>Time:</strong> {new Date(selectedTx.timestamp).toLocaleString()}</p>
              <p><strong>Amount:</strong> {selectedTx.amount} {wallet.coin_symbol}</p>
              <p><strong>Status:</strong> {selectedTx.confirmed? 'confirmed' : 'pending'}</p>
                <p><strong>Direction:</strong> {
                  selectedTx.sender === wallet.address || 
                  (selectedTx.hash.startsWith('fake-') && selectedTx.sender === "exchange") || 
                  (!selectedTx.hash.startsWith('fake-')) ? 
                  'Sent' : 'Received'
                }</p>
              <p><strong>{selectedTx.sender === wallet.address ? 'To:' : 'From:'}</strong> {selectedTx.sender === wallet.address ? selectedTx.receiver : selectedTx.sender}</p>
              {!selectedTx.hash.startsWith('fake-') && (
                <p><strong>https://blockstream.info/testnet/tx/${selectedTx.hash}</strong></p>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default WalletInfo;