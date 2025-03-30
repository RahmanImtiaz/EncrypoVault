import React from "react";
import { useState, ChangeEvent } from "react";
import useCryptoData from "./useCryptoData";
import LineGraph from "./graphs/linegraph";
import "../styles/BasicDetails.css";


// This is a functional component that will be shown to beginner users whenever they search for a certain cryptocurrency.
// The component will display basic information about the cryptocurrency, such as its name, symbol, description, current price, market cap, and 24-hour price change.

// The technical and more advanced details of the cryptocurrency will be displayed in a separate component called CryptoDetailsAdvanced.

// You will need to implement the function that will switch between the basic and advanced details of the cryptocurrency when the user clicks on a button.

// This will also provide the linegraph for the cryptocurrency and will allow the user to enter a time range to view the price history of the cryptocurrency.

//This time range will between 1 - 365 days.

interface BasicDetailsProps {
  cryptoId: string;
}
/*
interface CryptoData {
  name?: string;
  symbol?: string;
  image?: {
    small?: string;
  };
  market_data?: {
    current_price?: {
      gbp?: number;
    };
    price_change_percentage_24h?: number;
    market_cap?: {
      gbp?: number;
    };
    high_24h?: {
      gbp?: number;
    };
    low_24h?: {
      gbp?: number;
    };
  };
  description?: {
    en?: string;
  };
  market_cap_rank?: number;
  links?: {
    homepage?: string[];
    blockchain_site?: string[];
    official_forum_url?: string[];
    chat_url?: string[];
  };
}*/

const BasicDetails: React.FC<BasicDetailsProps> = ({ cryptoId }) => {
  const { cryptoData, isLoading, error } = useCryptoData(cryptoId);
  const [timeRange, setTimeRange] = useState<number>(30);

  // Alert box when loading
  if (isLoading) {
    return (
      <div className="loading">
        <p>Loading cryptocurrency data...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="error">
        <p>Error: {(error as Error).message}</p>
      </div>
    );
  }

  // Helper function to safely display nested data
  const getValue = (value: any): any =>
    value !== undefined && value !== null ? value : "N/A";

  return (
    <div className="basicDetails-container">
      <div className="crypto-header">
        <h1>
          {getValue(cryptoData?.name)} ({getValue(cryptoData?.symbol)?.toUpperCase()})
        </h1>
        {cryptoData?.image && cryptoData.image.small && (
          <img src={cryptoData.image.small} alt={cryptoData.name} />
        )}

        <div className="price-info">
            <p> Current Price: {getValue(cryptoData?.market_data?.current_price?.gbp)} </p>
        </div>
      </div>

      <div className="description">
        <p>
          {cryptoData?.description?.en
            ? cryptoData.description.en
            : "No description available."}
        </p>
      </div>

      <div className="graph-holder">
        <div className="time-range">
          <input
            type="number"
            min="1"
            max="365"
            value={timeRange}
            onChange={(e: ChangeEvent<HTMLInputElement>) => {
              const value = Math.max(1, Math.min(730, Number(e.target.value)));
              setTimeRange(value);
            }}
          />
        </div>

        <div className="line-graph">
          <LineGraph crypto_id={cryptoId} time_range={timeRange} />
        </div>
      </div>

      <div className="basic-info">
        <p>24h Price Change (%): {getValue(cryptoData?.market_data?.price_change_percentage_24h)}</p>
        <p>Market Cap Rank: {getValue(cryptoData?.market_cap_rank)}</p>
        <p>Market Cap (GBP): {getValue(cryptoData?.market_data?.market_cap?.gbp)}</p>
        <p>24h High (GBP): {getValue(cryptoData?.market_data?.high_24h?.gbp)}</p>
        <p>24h Low (GBP): {getValue(cryptoData?.market_data?.low_24h?.gbp)}</p>
      </div>

      <div className="links">
        <p>Homepage: {cryptoData?.links?.homepage?.[0] || "N/A"}</p>
        <p>Blockchain Site: {cryptoData?.links?.blockchain_site?.[0] || "N/A"}</p>
        <p>Official Forum: {cryptoData?.links?.official_forum_url?.[0] || "N/A"}</p>
        <p>Chat: {cryptoData?.links?.chat_url?.[0] || "N/A"}</p>
      </div>

    </div>
  );
};

export default BasicDetails;
