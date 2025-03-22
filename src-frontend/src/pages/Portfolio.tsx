//import React, { useState } from 'react';
import React from 'react';
import '../styles/Portfolio.css';
//import Wallet from '../Wallet';
//import {WalletType} from "../index";


/*
interface PortfolioProps {
  balance: number;
  wallets: WalletType[];
}*/

//const Portfolio: React.FC<PortfolioProps> = ({ balance, wallets }) => {
const Portfolio: React.FC = () => {
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

  return(
    <div className="portfolioContainer">
      <div className="balanceContainer">
        <h2 className="balanceHeading">Balance</h2>
        <p className="total">£1503.56</p>
      </div>
      <div className="tableContainer">
        some information
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