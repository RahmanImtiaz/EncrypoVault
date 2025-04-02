
 import useCryptoData from "./useCryptoData";
 import Candlestick from "./graphs/candlestick";

import { useState } from "react";

 
 // this is a functional component that will display both basic and advanced details of a cryptocurrency
 
 // once again the implementation to switch between the two will be done by someone else
 
 
 // this will also provide the candlestick graph option for the cryptocurrency
 
 // the time range will be between 1 - 30 days
 
 
interface AdvancedDetailsProps {
    cryptoId: string;
}

const AdvancedDetails = ({ cryptoId }: AdvancedDetailsProps) => {
     const { cryptoData, isLoading, error } = useCryptoData(cryptoId);
     const [timeRange, setTimeRange] = useState(30);
     const allowedDays = [1, 7, 14, 30, 90, 180, 365];
     console.log("received cryptoid", cryptoId);
    
     // alert box when loading
     if (isLoading) {
          return (
              <div className="loading">
                  <p>Loading cryptocurrency data...</p>
              </div>
          );
     }
 
     // alert box when error
     if (error) {
          return (
              <div className="error">
                  <p>Error: {(error as Error).message}</p>
              </div>
          );
     }
 
     // Helper function to safely display nested data
     const getValue = (value: any) => value !== undefined && value !== null ? value : "N/A";
 
     return (
         <div className="advancedDetails-container">
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
                     {cryptoData?.description && cryptoData.description.en
                         ? cryptoData.description.en
                         : "No description available."}
                 </p>
             </div>
 
             <div className="graph-holder">
                 <div className="time-range">
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
 
                 <div className="graph">
                 {cryptoId ? (
                    <Candlestick crypto_id={cryptoId} time_range={timeRange} />
                    ) : (
                      <p>No cryptocurrency selected.</p>
                    )}
                 </div>
             </div>
 
             <div className="basic-info">
                 <p>24h Price Change (%): {getValue(cryptoData?.market_data?.price_change_percentage_24h)}</p>
                 <p>Market Cap Rank: {getValue(cryptoData?.market_cap_rank)}</p>
                 <p>Market Cap (GBP): {getValue(cryptoData?.market_data?.market_cap?.gbp)}</p>
                 <p>24h High (GBP): {getValue(cryptoData?.market_data?.high_24h?.gbp)}</p>
                 <p>24h Low (GBP): {getValue(cryptoData?.market_data?.low_24h?.gbp)}</p>
             </div>
 
 
             <div className="technical-details">
                 <p>Hashing Algorithm: {getValue((cryptoData as any)?.hashing_algorithm)}</p>
 
                 <p>Block Time (seconds): {(cryptoData as any)?.block_time_in_minutes ? (cryptoData as any).block_time_in_minutes * 60 : "N/A"}</p>
 
                 <div className="categories">
                    <p>Categories: {Array.isArray(cryptoData?.categories) ? cryptoData.categories.join(", ") : "N/A"}</p>
                 </div>
 
             </div>
 
 
             <div className="ath-data">
                 <p> ATH Price: {getValue((cryptoData as any)?.market_data?.ath?.gbp)}</p>
 
                 <p> ATH Change Percentage: {getValue((cryptoData as any)?.market_data?.ath_change_percentage?.gbp)}</p>
                 
                 <p> ATH Date: {getValue((cryptoData as any)?.market_data?.ath_date?.gbp)}</p>
 
             </div>
 
             <div className="atl-data">
                 <p> ATL Price: {getValue((cryptoData as any)?.market_data?.atl?.gbp)}</p>
 
                 <p> ATL Change Percentage: {getValue((cryptoData as any)?.market_data?.atl_change_percentage?.gbp)}</p>
                 
                 <p> ATL Date: {getValue((cryptoData as any)?.market_data?.atl_date?.gbp)}</p>
             </div>
 
             <div className="market-data">
                 <p>Price Change: {getValue((cryptoData as any)?.market_data?.price_change_24h_in_currency?.gbp)}</p>
                 
                 <p> Fully Diluted Valuation: {((cryptoData as any)?.market_data?.fully_diluted_valuation?.gbp)}</p>
 
                 <p> Market Cap: {getValue(cryptoData?.market_data?.market_cap?.gbp)}</p>
 
                 <p> Market Cap Change: {getValue((cryptoData as any)?.market_data?.market_cap_change_24h_in_currency?.gbp)}</p>
 
                 <p> Market Cap Change Percentage: {getValue((cryptoData as any)?.market_data?.market_cap_change_percentage_24h)}</p>
 
 
             </div>
 
             <div className="supply-metrics">
                 <p> Circulating Supply: {getValue((cryptoData as any)?.market_data?.circulating_supply)}</p>
 
                 <p> Total Supply: {getValue((cryptoData as any)?.market_data?.total_supply)}</p>
 
                 <p> Max Supply: {getValue((cryptoData as any)?.market_data?.max_supply)}</p>
 
                 <p> Total Volume: {getValue((cryptoData as any)?.market_data?.total_volume?.gbp)}</p>
             </div>
 
 
             <div className="links">
                 <p>Homepage: {Array.isArray(cryptoData?.links?.homepage) && cryptoData.links.homepage.length > 0 ? cryptoData.links.homepage[0] : "N/A"}</p>
                 <p>Blockchain Site: {cryptoData?.links?.blockchain_site?.[0] || "N/A"}</p>
                 <p>Official Forum: {cryptoData?.links?.official_forum_url?.[0] || "N/A"}</p>
                 <p>Chat: {cryptoData?.links?.chat_url?.[0] || "N/A"}</p>
             </div>
         </div>
     );
 };
 
 export default AdvancedDetails;


