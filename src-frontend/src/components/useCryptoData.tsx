import { useState, useEffect } from "react";
import {Socket} from "socket.io-client";
//These files were previously in jsx, now I converted them into tsx. I had to add props to this file and the others.

interface CryptoData {
  id?: string;
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
    ath?: {
      gbp?: number;
    };
    ath_change_percentage?: {
      gbp?: number;
    };
    ath_date?: {
      gbp?: string;
    };
    atl?: {
      gbp?: number;
    };
    atl_change_percentage?: {
      gbp?: number;
    };
    atl_date?: {
      gbp?: string;
    };
    price_change_24h_in_currency?: {
      gbp?: number;
    };
    fully_diluted_valuation?: {
      gbp?: number;
    };
    market_cap_change_24h_in_currency?: {
      gbp?: number;
    };
    market_cap_change_percentage_24h?: number;
    circulating_supply?: number;
    total_supply?: number;
    max_supply?: number;
    total_volume?: {
      gbp?: number;
    };
  };
  market_cap_rank?: number;
  description?: {
    en?: string;
  };
  links?: {
    homepage?: string[];
    blockchain_site?: string[];
    official_forum_url?: string[];
    chat_url?: string[];
  };
  hashing_algorithm?: string;
  block_time_in_minutes?: number;
  categories?: string[];
}



interface useCryptoDataResult {
    cryptoData: CryptoData | null;
    isLoading: boolean;
    error: Error | null;
}





const useCryptoData = (crypto_id: string): useCryptoDataResult => {
    const[cryptoData, setCryptoData] = useState<CryptoData | null>(null);
    const[isLoading, setIsLoading] = useState(true);
    const[error, setError] = useState<Error | null>(null);

    useEffect(() => {
      if (!crypto_id) {
        setIsLoading(false);
        return;
      }
      
      setIsLoading(true);
    
      async function fetchCryptoData(){
        try{
          const socket = await window.api.getCryptoSocket() as Socket;
          socket.on("coin_data_response", (data: CryptoData) => {
            console.log("Received crypto data via socket:", data);
            setCryptoData(data);
            setIsLoading(false);
          });
          socket.emit("message", {
            command: "proxy_data",
            type: "coin_data",
            coin_id: crypto_id,
          });
        } catch (error) {
          console.error("Error fetching crypto data:", error);
          const errorMessage = error instanceof Error ? error : new Error("An unknown error occurred");
          setError(errorMessage);
          setIsLoading(false);
        }
      }
    
      fetchCryptoData();
    

    }, [crypto_id]);
    

    return { cryptoData, isLoading, error };
};



export default useCryptoData;