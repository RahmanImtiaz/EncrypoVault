// Portfolio.tsx
//import { useState } from 'react';
import React from 'react';
import '../styles/Market.css';
import BasicDetails from '../components/BasicDetails';
import { ChangeEvent } from 'react';

interface Coin {
  id: string;
  name: string;
  symbol: string;
}

//you need to use a ? to understand if a search value has been identified or not. Instead also, it can be that the user has a drop down showing all the current available crypto out there.
//
let searchValue: string | undefined = '';

const Market: React.FC = () => {
  const [coins, setCoins] = useState<Coin[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [searchInput, setSearchInput] = useState<string>("");
  const [filteredCoins, setFilteredCoins] = useState<Coin[]>([]);
  const [selectedCoin, setSelectedCoin] = useState<Coin | null>(null);

  useEffect(() => {
    fetch("https://api.coingecko.com/api/v3/coins/list")
      .then((response) => response.json())
      .then((data: Coin[]) => {
        setCoins(data);
        setLoading(false);
      })
      .catch((error) => {
        console.error("Error fetching coins:", error);
        setLoading(false);
      });
  }, []);

  // Update suggestions when searchInput or coins change
  useEffect(() => {
    if (selectedCoin && searchInput === selectedCoin.name) {
      setFilteredCoins([]);
      return;
    }
    if (searchInput.trim() === "") {
      setFilteredCoins([]);
      return;
    }
    const filtered = coins.filter((coin) =>
      coin.name.toLowerCase().includes(searchInput.toLowerCase())
    );
    setFilteredCoins(filtered);
  }, [searchInput, coins, selectedCoin]);

  const handleInputChange = (e: ChangeEvent<HTMLInputElement>) => {
    setSearchInput(e.target.value);

  };

  const handleSelectCoin = (coin: Coin) => {
    setSelectedCoin(coin);
    setSearchInput(coin.name);
    setFilteredCoins([]);
  };

  const handleInputFocus = () => {
    if (
      searchInput.trim() !== "" &&
      (!selectedCoin || searchInput !== selectedCoin.name)
    ) {
      const filtered = coins.filter((coin) =>
        coin.name.toLowerCase().includes(searchInput.toLowerCase())
      );
      setFilteredCoins(filtered);
    }
  };

  const handleInputBlur = () => {
    setTimeout(() => {
      setFilteredCoins([]);
    }, 200);
  };

  const handleClear = () => {
    setSearchInput("");
    setSelectedCoin(null);
    setFilteredCoins([]);
    searchValue = ''; // Reset the searchValue
    setLoading(true); // Show loading state temporarily
    
    // Reset loading state after a brief delay
    setTimeout(() => {
      setLoading(false);
    }, 300);
  };

  return (
    <div className="crypto-search-container">
      <h1 className="market-title">Markets</h1>
      <div className="search-section">
        <div className="search-box">
          <input
            type="text"
            value={searchInput}
            onChange={handleInputChange}
            onFocus={handleInputFocus}
            onBlur={handleInputBlur}
            placeholder="Type a Cryptocurrency name..."
            className="crypto-input"
          />
          <button 
            onClick={handleClear}
            className="clear-button"
          >
            Clear
          </button>
          {filteredCoins.length > 0 && (
            <div className="suggestions-box">
              {filteredCoins.slice(0, 10).map((coin) => (
                <div
                  key={coin.id}
                  className="suggestion-item"
                  onMouseDown={() => handleSelectCoin(coin)}
                >
                  {coin.name} ({coin.symbol.toUpperCase()})
                </div>
              ))}
            </div>
          )}
        </div>
      </div>

      <div className="details-section">
        {loading ? (
          <div className="placeholder">
            <p>Loading cryptocurrencies...</p>
          </div>
        ) : (
          <BasicDetails cryptoId={selectedCoin?.id || searchValue || ""} />
        )}
      </div>
    </div>
  );
};


export default Market;
function useState<T>(initialValue: T): [T, React.Dispatch<React.SetStateAction<T>>] {
  const [state, setState] = React.useState<T>(initialValue);
  return [state, setState];
}
function useEffect(effect: () => void | (() => void), deps: React.DependencyList) {
  React.useEffect(effect, deps);
}

