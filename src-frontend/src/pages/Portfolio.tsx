import React, { useState, useEffect } from 'react';
import { useNavigate } from "react-router-dom";
import { QRCodeComponent } from '../components/generateQR';
import useCryptoPrice from '../components/fetchPrice';
import "../styles/Portfolio.css";
import { getWalletBalance } from '../components/helpers/FakeTransactionRecords';
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
  fake_balance: number;
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
  confirmed?: boolean;
}

const Portfolio: React.FC = () => {
  const { priceData } = useCryptoPrice();
  const navigate = useNavigate();
  //const [aggregatedHoldings, setAggregatedHoldings] = useState<AggregatedHolding[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [accountType, setAccountType] = useState<string>("");
  const [showTransactionHistory, setShowTransactionHistory] = useState<boolean>(false);
  const [showWalletList, setShowWalletList] = useState<boolean>(false);
  const [transactionType, setTransactionType] = useState<string>("");
  const [wallets, setWallets] = useState<Wallet[]>([]);
  const [chosenWallet, setChosenWallet] = useState<Wallet | null>(null);
  const [showQR, setShowQR] = useState(false);
  const [totalBalance, setTotalBalance] = useState<number>(0);
  const [transactions, setTransactions] = useState<Transaction[]>([]);
  const savedTheme = localStorage.getItem('theme');

  const checkConfirmationStatus = async (txid: string): Promise<boolean> => {
    try {
      const response = await fetch(`https://blockstream.info/testnet/api/tx/${txid}/status`);
      const data = await response.json();
      return data.confirmed === true;
    } catch (err) {
      console.error(`Failed to check status for txid ${txid}:`, err);
      return false; 
    }
  };
  

  const fetchWallets = async () => {
    try {
      setLoading(true);
      const walletsList: Wallet[] = await api.getWallets();
      console.log("Fetched wallets:", walletsList); 
      setWallets(walletsList);
  
      // Wait for price data to be available
      if (!priceData) {
        console.warn("Price data is not available. Using wallet balances without conversion.");
        setTotalBalance(
          walletsList.reduce((sum, wallet) => sum + wallet.balance + Number(wallet.fake_balance), 0)
        );
        return;
      }
  
      // Calculate total balance using price data
      const total = walletsList.reduce((sum, wallet) => {
        const priceKey = wallet.coin_symbol === "BTC" ? "BTC-GBP" : "ETH-GBP";
        const price = priceData?.[priceKey];
  
        if (price === undefined) {
          console.warn(`Price for ${wallet.coin_symbol} is undefined. Using wallet balance directly.`);
        }
  
        const walletBalance = price !== undefined
          ? (Number(wallet.balance) + Number(wallet.fake_balance)) * Number(price) // Convert to GBP
          : wallet.balance + Number(wallet.fake_balance); // Fallback to native balance
  
        console.log(`Wallet: ${wallet.name}, Balance: ${wallet.balance}, Fake Balance: ${wallet.fake_balance}, Price: ${price}, Wallet Balance in GBP: ${walletBalance}`);
        return sum + walletBalance;
      }, 0);
  
      console.log("Calculated total balance:", total);
      setTotalBalance(total);
    } catch (err) {
      console.error("Error fetching wallets:", err);
      setError("Failed to load wallets");
    } finally {
      setLoading(false);
    }
  };

  const fetchTransactions = async () => {
    try {
      const allTransactions: Transaction[] = await api.getAllTransactions();
  
      const transactionsWithStatus = await Promise.all(
        allTransactions.map(async (tx) => {
          const isFakeTx = tx.hash.startsWith('fake-');
          let confirmed = true;
  
          if (!isFakeTx) {
            const txid = tx.hash;
            confirmed = await checkConfirmationStatus(txid);
          }
  
          return { ...tx, confirmed };
        })
      );
  
      setTransactions(transactionsWithStatus);
    } catch (error) {
      console.error('Error fetching transactions:', error);
    }
  };
  

  const refreshData = async () => {
    await fetchWallets();
    await fetchTransactions();
  };
  
  useEffect(() => {
    refreshData();
  }, [priceData]);

  useEffect(() => {
    if (savedTheme === 'light')
      document.body.classList.add('light-mode');
    else
      document.body.classList.remove('light-mode');
  }, [savedTheme]);

  useEffect(() => {
    if (localStorage.getItem('theme') === 'light')
      document.body.classList.add('light-mode');
    else
      document.body.classList.remove('light-mode');
  })

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        await fetchAccountType();
        //await fetchPortfolioData();
      }
      catch (err) {
        setError("Failed to load portfolio data");
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  const fetchAccountType = async () => {
    try {
      const response = await fetch('/api/accounts/current');
      const accountData = await response.json();
      if (accountData?.accountType) {
        setAccountType(accountData.accountType);
      }
    } catch (error) {
      console.error("Failed to fetch account type:", error);
    }
  };

  const toggleTransactionHistory = () => {
    setShowTransactionHistory(!showTransactionHistory);
  };

  const youtubeVideos = [
    { title: "Crypto Investing for Beginners", url: "https://www.youtube.com/watch?v=LGHsNaIv5os" },
    { title: "Crypto Trading", url: "https://www.youtube.com/watch?v=DRAcPbYPNVk" },
    { title: "Understanding Blockchain", url: "https://www.youtube.com/watch?v=yubzJw0uiE4&pp=ygUkdW5kZXJzdGFkbmluZyBiaXRjb2luIGFuZCBibG9ja2NoYWlu" },
  ];

  const expandWallets = (transaction: string) => {
    setShowWalletList(true);
    setTransactionType(transaction);
  };

  const handleWalletSelect = (wallet: Wallet) => {
    setChosenWallet(wallet);
    switch (transactionType) {
      case "receive":
        setShowQR(true);
        break;
      case "send":
        navigate('/send', { state: { wallet } });
        break;
      case "buy":
        navigate('/buy', { state: { wallet } });
        break;
      case "sell":
        navigate('/sell', { state: { wallet } });
        break;
      default:
        console.warn('Unknown transaction type');
    }
  };

  if (loading) {
    return (
      <div className="portfolioContainer">
        <p className="loading">Loading portfolio data...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="portfolioContainer">
        <p className="error">{error}</p>
      </div>
    );
  }

  if (showQR && chosenWallet) {
    return (
      <div className="qr-modal-overlay">
        <div className="qr-modal-content">
          <div className="modal-header">
            <h2>{chosenWallet.name}</h2>
          </div>
          <QRCodeComponent
            value={chosenWallet.address}
            size={256}
            level="Q"
            bgColor="#FFFFFF"
            fgColor="#000000"
          />
          <p className="address-text">Wallet Address: {chosenWallet.address}</p>
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

  if (showWalletList) {
    return (
      <div className="wallets-list-overlay">
        <div className="wallet-list-container">
          {wallets.length === 0 ? (
            <div className="empty-wallet-list">
              <p>No wallets found.</p>
            </div>
          ) : (
            <div className="all-wallets-list">
              {wallets.map((wallet, index) => (
                <div
                  key={index}
                  className="single-wallet-item"
                  onClick={() => handleWalletSelect(wallet)}
                >
                  <div className="single-wallet-header">
                    <h3 className="single-wallet-name">{wallet.name}</h3>
                    <span className="single-wallet-balance">
                      {(() => {
                        const priceKey = wallet.coin_symbol === "BTC" ? "BTC-GBP" : "ETH-GBP";
                        const price = priceData?.[priceKey];
                        return `£${(wallet.balance * Number(price || 1)).toFixed(2)}`;
                      })()}
                    </span>
                  </div>
                  <div className="single-wallet-content">
                    <div className="wallet-details-important">
                      <div className="wallet-details-row">
                        <span className="wallet-details-label">Type:</span>
                        <span className="wallet-details-value">{wallet.coin_symbol}</span>
                      </div>
                      <div className="wallet-details-row">
                        <span className="wallet-details-label">Holdings:</span>
                        <span className="wallet-details-value">
                          {getWalletBalance(wallet)} {wallet?.coin_symbol}
                        </span>
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
          <button className="close-wallet-list-button" onClick={() => setShowWalletList(false)}>x</button>
        </div>
      </div>
    );
  }

  return (
    <div className="portfolioContainer">
      <div className="balanceContainer">
        <h2 className="balanceHeading">Total Balance</h2>
        <p className="total">£{totalBalance.toFixed(2)}</p>
        <p className="rate-disclaimer">when offline, rates may not be the most accurate</p>
      </div>

      {accountType && (
        <div className="account-type-badge" data-type={accountType}>
          {accountType} Mode
        </div>
      )}

      <div className="quickActions">
        <h2>Quick Actions</h2>
        <div className="actionButtons">
          <button className="actionButton" onClick={() => expandWallets("buy")}>Buy Crypto</button>
          <button className="actionButton" onClick={() => expandWallets("sell")}>Sell Crypto</button>
          <button className="actionButton" onClick={() => expandWallets("send")}>Send Crypto</button>
          <button className="actionButton" onClick={() => expandWallets("receive")}>Receive Crypto</button>
        </div>
      </div>

      {accountType === "Beginner" && (
        <div className="youtubeVideos">
          <h2>Learn Crypto Trading</h2>
          <ul>
            {youtubeVideos.map((video, index) => (
              <li key={index}>
                <p>
                  <strong>{video.title}:</strong> {video.url}
                </p>
              </li>
            ))}
          </ul>
        </div>
      )}

      <div className="transaction-history">
        <button className="toggleButton" onClick={toggleTransactionHistory}>
          {showTransactionHistory ? "Hide Transaction History" : "Show Transaction History"}
        </button>
        {showTransactionHistory && (
          <>
            <h3>Transaction History</h3>
            {transactions.length === 0 ? (
              <p className="no-transactions">No transactions yet</p>
            ) : (
              <div className="transactions-list">
                {transactions.map((tx) => {
                  const wallet = wallets.find(w => w.name === tx.name);
                  const isOutgoing = wallet ? tx.sender === wallet.address : false;
                  const isFakeBuy = tx.sender === "exchange";
                  const isFakeSell = tx.receiver === "exchange";
                  const isConfirmed = true;

                  return (
                    <div
                      key={tx.hash}
                      className={`transaction-item ${
                        isOutgoing ? 'out' : 'in'
                      } ${
                        isFakeBuy ? 'fake-buy' : isFakeSell ? 'fake-sell' : ''
                      }`}
                    >
                      <div className="tx-direction">
                        {isOutgoing ? '⬆️' : '⬇️'}
                      </div>
                      <div className="tx-details">
                        <div className="tx-amount">
                          {isOutgoing ? '-' : '+'}{tx.amount} {wallet?.coin_symbol || 'CRYPTO'}
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
                        {tx.confirmed ? 'confirmed' : 'pending'}
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
          </>
        )}
      </div>
    </div>
  );
};

export default Portfolio;