import React, { useState, useEffect } from 'react';
import { useNavigate } from "react-router-dom";
import { QRCodeComponent } from '../components/generateQR';
import useCryptoPrice from '../components/fetchPrice';
import "../styles/Portfolio.css";

interface Holding{
  amount: number;
  name: string;
  symbol: string;
  value: number;
}

interface Wallet{
  name: string;
  balance: number;
  address: string;
  coin_symbol: string;
  holdings: {
    [key: string]: Holding;
  };
}

interface AggregatedHolding extends Holding {
  percentOfPortfolio: number;
  wallets: { name: string; amount: number }[];
}


const Portfolio: React.FC = () => {
  const {priceData} = useCryptoPrice();
  const navigate = useNavigate();
  const [balance, setBalance] = useState<number>(0);
  const [aggregatedHoldings, setAggregatedHoldings] = useState<AggregatedHolding[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [accountType, setAccountType] = useState<string>("");
  const [expandedAsset, setExpandedAsset] = useState<string | null>(null);
  const [showTransactionHistory, setShowTransactionHistory] = useState<boolean>(false);
  const [showWalletList, setShowWalletList] = useState<boolean>(false);
  const [transactionType, setTransactionType] = useState<string>("");
  const [wallets, setWallets] = useState<Wallet[]>([]);
  const [chosenWallet, setChosenWallet] = useState<Wallet | null>(null);
  const [showQR, setShowQR] = useState(false);
  const savedTheme = localStorage.getItem('theme');
 
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
        await fetchPortfolioData();
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

  const fetchPortfolioData = async () => {
    try {
      const balance = await window.api.getPortfolioBalance();

      const wallets: Wallet[] = await window.api.getWallets();
      setWallets(wallets);

      const holdings: { [key: string]: AggregatedHolding } = {};
      wallets.forEach((wallet) => {
        Object.entries(wallet.holdings).forEach(([cryptoId, holding]) => {
          if (!holdings[cryptoId]) {
            holdings[cryptoId] = {
              name: holding.name,
              symbol: holding.symbol,
              amount: 0,
              value: 0,
              percentOfPortfolio: 0,
              wallets: [],
            };
          }
          holdings[cryptoId].amount += holding.amount;
          holdings[cryptoId].value += holding.value;
          holdings[cryptoId].wallets.push({
            name: wallet.name,
            amount: holding.amount,
          });
        });
      });

      const holdingsArray = Object.values(holdings);
      holdingsArray.forEach((holding) => {
        holding.percentOfPortfolio = balance > 0 ? (holding.value / balance) * 100 : 0;
      });

      holdingsArray.sort((a, b) => b.value - a.value);
      setBalance(balance);
      setAggregatedHoldings(holdingsArray);
    } catch (err) {
      console.error("Error fetching portfolio data:", err);
      throw err;
    }
  };

  
  const toggleAssetDetails = (symbol: string) => {
    setExpandedAsset(expandedAsset === symbol ? null : symbol);
  };

  const toggleTransactionHistory = () => {
    setShowTransactionHistory(!showTransactionHistory);
  };

  const youtubeVideos = [
    { title: "Crypto Investing for Beginners", url: "https://www.youtube.com/watch?v=LGHsNaIv5os" },
    { title: "Crypto Trading", url: "https://www.youtube.com/watch?v=DRAcPbYPNVk" },
    { title: "Understanding Blockchain", url: "https://www.youtube.com/watch?v=yubzJw0uiE4&pp=ygUkdW5kZXJzdGFkbmluZyBiaXRjb2luIGFuZCBibG9ja2NoYWlu" },
  ];

  const transactionHistory = [
    { id: 1, date: "2025-04-01", type: "Buy", amount: "0.1 BTC", value: "£3000" },
    { id: 2, date: "2025-03-28", type: "Sell", amount: "0.05 ETH", value: "£100" },
    { id: 3, date: "2025-03-25", type: "Receive", amount: "100 ADA", value: "£50" },
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
                            {wallet.balance} {wallet.coin_symbol}
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
        <p className="total">£{balance.toFixed(2)}</p>
      </div>

      {/* Account Type Badge */}
      
      {accountType && (
          <div className="account-type-badge" data-type={accountType}>
            {accountType} Mode
          </div>
      )}

      <div className="portfolioComposition">
        <h2>Portfolio Composition</h2>
        {aggregatedHoldings.length === 0 ? (
          <p>No crypto holdings found in your wallets.</p>
        ) : (
          <div className="holdingsList">
            {aggregatedHoldings.map((holding) => (
              <div key={holding.symbol} className="holdingItem">
                <div
                  className="holdingSummary"
                  onClick={() => toggleAssetDetails(holding.symbol)}
                >
                  <h3>
                    {holding.name} ({holding.symbol.toUpperCase()})
                  </h3>
                  <p>
                    {holding.amount.toFixed(8)} {holding.symbol.toUpperCase()} - £
                    {holding.value.toFixed(2)} ({holding.percentOfPortfolio.toFixed(1)}%)
                  </p>
                </div>

                {expandedAsset === holding.symbol && (
                  <div className="holdingDetails">
                    <h4>Wallet Breakdown</h4>
                    <ul>
                      {holding.wallets.map((wallet, index) => (
                        <li key={index}>
                          {wallet.name}: {wallet.amount.toFixed(8)} {holding.symbol.toUpperCase()}
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            ))}
          </div>
        )}
      </div>

      <div className="quickActions">
        <h2>Quick Actions</h2>
        <div className="actionButtons">
          <button className="actionButton" onClick={() => expandWallets("buy")}>Buy Crypto</button>
          <button className="actionButton" onClick={() => expandWallets("sell")}>Sell Crypto</button>
          <button className="actionButton" onClick={() => expandWallets("send")}>Send Crypto</button>
          <button className="actionButton" onClick={() => expandWallets("receive")}>Receive Crypto</button>
        </div>
      </div>

      {/* YouTube Videos Section */}
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

      {/* Transaction History Section */}
      <div className="transactionHistory">
        <button className="toggleButton" onClick={toggleTransactionHistory}>
          {showTransactionHistory ? "Hide Transaction History" : "Show Transaction History"}
        </button>
        {showTransactionHistory && (
          <ul className="transactionList">
            {transactionHistory.map((transaction) => (
              <li key={transaction.id}>
                <p>
                  <strong>Date:</strong> {transaction.date}
                </p>
                <p>
                  <strong>Type:</strong> {transaction.type}
                </p>
                <p>
                  <strong>Amount:</strong> {transaction.amount}
                </p>
                <p>
                  <strong>Value:</strong> {transaction.value}
                </p>
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );


};


export default Portfolio;