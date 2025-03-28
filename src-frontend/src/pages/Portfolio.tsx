//import React, { useState } from 'react';
import React, { useState, useEffect } from 'react';
import '../styles/Portfolio.css';
//import Wallet from '../Wallet';
//import {WalletType} from "../index";


/*
interface PortfolioProps {
  balance: number;
  wallets: WalletType[];
}*/

interface Holding {
  amount: number;
  name: string;
  symbol: string;
  value: number;
}

interface AggregatedHolding extends Holding {
  percentOfPortfolio: number;
}

//const Portfolio: React.FC<PortfolioProps> = ({ balance, wallets }) => {
const Portfolio: React.FC = () => {
  const [balance, setBalance] = useState<number>(0);
  const [aggregatedHoldings, setAggregatedHoldings] = useState<AggregatedHolding[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  /*
  const [selectedWallet, setSelectedWallet] = useState<number | null>(null);

  const handleWalletClick = (index: number) => {
    setSelectedWallet(selectedWallet === index ? null : index);
  };

  const handleSend = (walletIndex: number) => {
    // Implement send functionality
    console.log(`Send from wallet ${wallets[walletIndex].name}`);
  };

  const handleReceive = (walletIndex: number) => {
    // Implement receive functionality
    console.log(`Receive to wallet ${wallets[walletIndex].name}`);
  };

  const handleTrade = (walletIndex: number) => {
    // Implement trade functionality
    console.log(`Trade from wallet ${wallets[walletIndex].name}`);
  };*/

  useEffect(() => {
    fetchPortfolioData();
  }, []);

  const fetchPortfolioData = async () => {
    try {
      setLoading(true);
      
      // Just fetch the balance
      const balance = await window.api.get_portfolio_balance();
      
      // Get wallets to calculate aggregated holdings
      const wallets = await window.api.get_portfolio_wallets();
      
      // Calculate aggregated holdings across all wallets
      const holdings: {[key: string]: AggregatedHolding} = {};
      
      wallets.forEach((wallet: { holdings: { [key: string]: Holding } }) => {
        Object.entries(wallet.holdings).forEach(([cryptoId, holding]) => {
          if (!holdings[cryptoId]) {
            holdings[cryptoId] = {
              name: holding.name,
              symbol: holding.symbol,
              amount: 0,
              value: 0,
              percentOfPortfolio: 0
            };
          }
          holdings[cryptoId].amount += holding.amount;
          holdings[cryptoId].value += holding.value;
        });
      });
      
      // Calculate percentage of portfolio
      const holdingsArray = Object.values(holdings);
      holdingsArray.forEach(holding => {
        holding.percentOfPortfolio = balance > 0 ? (holding.value / balance) * 100 : 0;
      });
      
      // Sort by value (highest first)
      holdingsArray.sort((a, b) => b.value - a.value);
      
      setBalance(balance);
      setAggregatedHoldings(holdingsArray);
      setError(null);
    } catch (err) {
      console.error('Error fetching portfolio data:', err);
      setError('Failed to load portfolio data');
    } finally {
      setLoading(false);
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

  return (
    <div className="portfolioContainer">
      {/* Balance Section */}
      <div className="balanceContainer">
        <h2 className="balanceHeading">Total Balance</h2>
        <p className="total">£{balance.toFixed(2)}</p>
      </div>
      
      {/* Portfolio Composition Section */}
      <div className="portfolioComposition">
        <h2>Portfolio Composition</h2>
        {aggregatedHoldings.length === 0 ? (
          <p>No crypto holdings found in your wallets.</p>
        ) : (
          <div className="holdingsGrid">
            {aggregatedHoldings.map(holding => (
              <div key={holding.symbol} className="holdingCard">
                <div className="holdingHeader">
                  <h3>{holding.name} ({holding.symbol.toUpperCase()})</h3>
                  <div className="percentBadge">{holding.percentOfPortfolio.toFixed(1)}%</div>
                </div>
                <p className="holdingAmount">{holding.amount.toFixed(8)} {holding.symbol.toUpperCase()}</p>
                <p className="holdingValue">£{holding.value.toFixed(2)}</p>
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
        </div>
      </div>
    </div>
  );

  /*
  return (
    <div className="portfolio-container">
      <h1 className="portfolio-title">Portfolio</h1>
      <div className="portfolio-summary">
        <div className="portfolio-balance">
          <h3>Total Balance</h3>
          <p className="balance-amount">${balance.toFixed(2)}</p>
        </div>
        <div className="portfolio-stats">
          <div className="stat-item">
            <span>24h Change</span>
            <span className="positive">+2.5%</span>
          </div>
          <div className="stat-item">
            <span>Active Wallets</span>
            <span>{wallets.length}</span>
          </div>
        </div>
      </div>
      <div className="wallets-container">
        <h2 className="portfolio-subtitle">Your Wallets</h2>
        <div className="wallet-grid">
          {wallets.map((wallet, index) => (
            <Wallet
              key={index}
              name={wallet.name}
              balance={wallet.balance}
              address={wallet.address}
              transactions={wallet.transactions}
              isSelected={selectedWallet === index}
              onClick={() => handleWalletClick(index)}
              onSend={() => handleSend(index)}
              onReceive={() => handleReceive(index)}
              onTrade={() => handleTrade(index)}
            />
          ))}
        </div>
      </div>
    </div>
  );
  */
};

export default Portfolio;