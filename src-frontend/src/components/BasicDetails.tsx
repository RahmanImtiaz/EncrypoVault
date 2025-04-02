import React from "react";
import { useState, ChangeEvent } from "react";
import useCryptoData from "./useCryptoData";
import LineGraph from "./graphs/linegraph";
import "../styles/BasicDetails.css";



interface BasicDetailsProps {
  cryptoId: string;
}


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
