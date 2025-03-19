import React from 'react';
import './Portfolio.css';

interface Transaction {
  date: string;
  type: 'send' | 'receive' | 'trade';
  amount: number;
  status: 'completed' | 'pending' | 'failed';
}

interface WalletProps {
  name: string;
  balance: number;
  address?: string;
  transactions?: Transaction[];
  isSelected: boolean;
  onClick: () => void;
  onSend: () => void;
  onReceive: () => void;
  onTrade: () => void;
}

const Wallet: React.FC<WalletProps> = ({
  name,
  balance,
  address,
  transactions,
  isSelected,
  onClick,
  onSend,
  onReceive,
  onTrade
}) => {
  return (
    <div className={`wallet-card ${isSelected ? 'wallet-selected' : ''}`} onClick={onClick}>
      <div className="wallet-header">
        <div className="wallet-title">
          <img 
            src={`/crypto-icons/${name.toLowerCase()}.svg`} 
            alt={name}
            className="wallet-icon"
          />
          <h3>{name}</h3>
        </div>
        <span className="wallet-balance">${balance.toFixed(2)}</span>
      </div>
      
      {isSelected && (
        <div className="wallet-details">
          {address && (
            <div className="wallet-address">
              <span>Address:</span>
              <code>{address}</code>
            </div>
          )}
          
          <div className="wallet-actions">
            <button onClick={(e) => { e.stopPropagation(); onSend(); }} className="action-button send">
              Send
            </button>
            <button onClick={(e) => { e.stopPropagation(); onReceive(); }} className="action-button receive">
              Receive
            </button>
            <button onClick={(e) => { e.stopPropagation(); onTrade(); }} className="action-button trade">
              Trade
            </button>
          </div>

          {transactions && transactions.length > 0 && (
            <div className="transactions-list">
              <h4>Recent Transactions</h4>
              {transactions.map((tx, index) => (
                <div key={index} className={`transaction-item ${tx.status}`}>
                  <span className="transaction-type">{tx.type}</span>
                  <span className="transaction-amount">${tx.amount.toFixed(2)}</span>
                  <span className="transaction-date">{tx.date}</span>
                  <span className="transaction-status">{tx.status}</span>
                </div>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default Wallet;