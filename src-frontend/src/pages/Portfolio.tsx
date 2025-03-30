import React, { useState, useEffect } from 'react';
import '../styles/Portfolio.css';
import { useNavigate } from "react-router-dom";

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
  
  const navigate = useNavigate();

  useEffect(() => {
    fetchPortfolioData();
  }, []);

  const fetchPortfolioData = async () => {
    try {
      setLoading(true);
      
      // Just fetch the balance
      const balance = await window.api.getPortfolioBalance();
      
      // Get wallets to calculate aggregated holdings
      const wallets = await window.api.getPortfolioWallets();
      
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
          <button className="actionButton" onClick={() => navigate("/buy")}>Buy Crypto</button>
          <button className="actionButton" onClick={() => navigate("/sell")}>Sell Crypto</button>
          <button className="actionButton" onClick={() => navigate("/send")}>Send Crypto</button>
          <button className="actionButton" onClick={() => navigate("/receive")}>Receive Crypto</button>
        </div>
      </div>
    </div>
  );
};

export default Portfolio;