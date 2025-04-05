import React, { useState, useEffect } from "react";
import "../styles/Portfolio.css";

interface Holding {
  amount: number;
  name: string;
  symbol: string;
  value: number;
}

interface Wallet {
  name: string;
  holdings: { [key: string]: Holding };
}

interface AggregatedHolding extends Holding {
  percentOfPortfolio: number;
  wallets: { name: string; amount: number }[];
}

const Portfolio: React.FC = () => {
  const [balance, setBalance] = useState<number>(0);
  const [aggregatedHoldings, setAggregatedHoldings] = useState<AggregatedHolding[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [accountType, setAccountType] = useState<string>("");
  const [expandedAsset, setExpandedAsset] = useState<string | null>(null);
  const [showTransactionHistory, setShowTransactionHistory] = useState<boolean>(false);

  useEffect(() => {
    fetchPortfolioData();
    fetchAccountType();
  }, []);

  const fetchAccountType = async () => {
    try {
      const response = await fetch('/api/accounts/current');
      const accountData = await response.json();

      if (accountData && accountData.accountType) {
        setAccountType(accountData.accountType);
      }
    } catch (error) {
      console.error("Failed to fetch account type:", error);
    }
  };

  const fetchPortfolioData = async () => {
    try {
      setLoading(true);

      // Fetch the total balance
      const balance = await window.api.getPortfolioBalance();

      // Fetch wallets and their holdings
      const wallets: Wallet[] = await window.api.getPortfolioWallets();

      // Aggregate holdings across all wallets
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

      // Calculate percentage of portfolio
      const holdingsArray = Object.values(holdings);
      holdingsArray.forEach((holding) => {
        holding.percentOfPortfolio = balance > 0 ? (holding.value / balance) * 100 : 0;
      });

      // Sort holdings by value (highest first)
      holdingsArray.sort((a, b) => b.value - a.value);

      // Update state
      setBalance(balance);
      setAggregatedHoldings(holdingsArray);
      setError(null);
    } catch (err) {
      console.error("Error fetching portfolio data:", err);
      setError("Failed to load portfolio data");
    } finally {
      setLoading(false);
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

  return (
    <div className="portfolioContainer">
      {/* Balance Section */}
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
      {/* Portfolio Composition Section */}
      <div className="portfolioComposition">
        <h2>Portfolio Composition</h2>
        {aggregatedHoldings.length === 0 ? (
          <p>No crypto holdings found in your wallets.</p>
        ) : (
          <div className="holdingsList">
            {aggregatedHoldings.map((holding) => (
              <div key={holding.symbol} className="holdingItem">
                {/* Asset Summary */}
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

                {/* Asset Details (Dropdown) */}
                {expandedAsset === holding.symbol && (
                  <div className="holdingDetails">
                    <h4>Wallet Breakdown</h4>
                    <ul>
                      {holding.wallets.map((wallet, index) => (
                        <li key={index}>
                          {wallet.name}: {wallet.amount.toFixed(8)}{" "}
                          {holding.symbol.toUpperCase()}
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

      {/* Quick Actions Section */}
      <div className="quickActions">
        <h2>Quick Actions</h2>
        <div className="actionButtons">
          <button className="actionButton">Buy Crypto</button>
          <button className="actionButton">Sell Crypto</button>
          <button className="actionButton">Send Crypto</button>
          <button className="actionButton">Receive Crypto</button>
        </div>
      </div>

      {/* YouTube Videos Section */}
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