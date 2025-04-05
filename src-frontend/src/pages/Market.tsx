

import React from 'react';
import '../styles/Market.css';
import BasicDetails from '../components/BasicDetails';
import { ChangeEvent } from 'react';
import AdvancedDetails from '../components/AdvancedDetails';
import { Socket } from 'socket.io-client';

interface Coin {
  id: string;
  name: string;
  symbol: string;
}

//you need to use a ? to understand if a search value has been identified or not. Instead also, it can be that the user has a drop down showing all the current available crypto out there.
//


const Market: React.FC = () => {
  const [coins, setCoins] = useState<Coin[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [searchInput, setSearchInput] = useState<string>("");
  const [filteredCoins, setFilteredCoins] = useState<Coin[]>([]);
  const [selectedCoin, setSelectedCoin] = useState<Coin | null>(null);
  const [accountType, setAccountType] = useState<string>("");
  const savedTheme = localStorage.getItem('theme');

  useEffect(() => {
    if (savedTheme === 'light')
      document.body.classList.add('light-mode');
    else 
      document.body.classList.remove('light-mode');
  }, [savedTheme]);


  useEffect(() => {
    async function fetchCoins() {
      try {
        const socket = await window.api.getCryptoSocket() as Socket;
        socket.on("coins_list_response", (data: Coin[]) => {
          console.log("Received coins list via socket:", data);
          setCoins(data);
          setLoading(false);
        });


        socket.emit("message", {
          command: "proxy_data",
          type: "coins_list"
        });
      } catch (error) {
        console.error("Error fetching coins:", error);
        setLoading(false);
      }
    }

    fetchCoins();
  }, []);
  

  useEffect(() => {
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
    console.log("Selected coin:", coin);
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

    setLoading(true); // Show loading state temporarily
    
    // Reset loading state after a brief delay
    setTimeout(() => {
      setLoading(false);
    }, 300);
    console.log(selectedCoin)
  };

  return (
    <div className="crypto-search-container">
      <h1 className="market-title">Market</h1>
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
        <h2 className="details-title">Description</h2>
        {loading ? (
          <div className="placeholder">
            <p>Loading cryptocurrencies...</p>
          </div>
        ) : selectedCoin ? (
          accountType === "Beginner" ? (
            <BasicDetails cryptoId={selectedCoin.id} />
          ) : (
            <AdvancedDetails cryptoId={selectedCoin.id} />
          )
        ) : (
          <div className="placeholder">
            <p>Select a cryptocurrency to view details</p>
          </div>
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

