import { useState, useEffect } from 'react';
import Candlestick from './components/candlestick'; 
import LineGraph from './components/linegraph';


const Graph = () => {
  const [cryptos, setCryptos] = useState([]);
  const [timeRange, setTimeRange] = useState(30);
  const [selectedCrypto, setSelectedCrypto] = useState(null);
  const [selectedGraph, setSelectedGraph] = useState('line');

  useEffect(() => {
    const fetchData = async () => {
      try {
        const options = {
          method: 'GET',
          headers: {
            accept: 'application/json',
            'x-cg-demo-api-key': 'CG-E46h8ehSNZFLW8b3zrv1xzyP'
          }
        };

        const response = await fetch(
          'https://api.coingecko.com/api/v3/coins/markets?vs_currency=gbp',
          options
        );
        const data = await response.json();
        setCryptos(data);
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };

    fetchData();
  }, []);

  const allowedDays = [1, 7, 14, 30, 90, 180, 365];

  return (
    <>
      <div>
        <select
          value={selectedCrypto ? selectedCrypto.id : 'DEFAULT'}
          onChange={(e) => {
            const crypto = cryptos.find((x) => x.id === e.target.value);
            setSelectedCrypto(crypto);
          }}
        >
          <option value="DEFAULT" disabled>
            Select a crypto...
          </option>
          {cryptos.map((crypto) => (
            <option key={crypto.id} value={crypto.id}>
              {crypto.name} ({crypto.symbol.toUpperCase()})
            </option>
          ))}
        </select>
      </div>


      <div>
        <select
          onChange={(e) => setSelectedGraph(e.target.value)}
          value={selectedGraph}
        >
          <option value="line">Line Graph</option>
          <option value="candlestick">Candlestick</option>
        </select>
      </div>

      {selectedGraph === 'candlestick' && (
        <div>
          <select
        value={timeRange}
        onChange={(e) => setTimeRange(Number(e.target.value))}
          >
        {allowedDays.map((day) => (
          <option key={day} value={day}>
            {day} day{day > 1 ? 's' : ''}
          </option>
        ))}
          </select>
        </div>
      )}

      {selectedGraph === 'line' && (
        <div>
          <input
        type="number"
        min="1"
        max="365"
        value={timeRange}
        onChange={(e) => {
          const value = Math.max(1, Math.min(730, Number(e.target.value)));
          setTimeRange(value);
        }}
          />
        </div>
      )}


      {selectedCrypto && selectedGraph === 'line' && (
        <LineGraph crypto_id={selectedCrypto.id} time_range={timeRange} />
      )}

      {selectedCrypto && selectedGraph === 'candlestick' && (
        <Candlestick crypto_id={selectedCrypto.id} time_range={timeRange} />
      )}

    </>
  );
};

export default Graph;
