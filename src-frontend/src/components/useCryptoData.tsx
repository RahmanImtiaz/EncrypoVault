import { useState, useEffect } from "react";
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
  }


interface useCryptoDataResult {
    cryptoData: CryptoData | null;
    isLoading: boolean;
    error: Error | null;
}





const useCryptoData = (crypto_id: string): useCryptoDataResult => {
    const[cryptoData, setCryptoData] = useState<CryptoData | null>(null);
    const[isLoading, setIsLoading] = useState(true);
    const[error, setError] = useState(null);

    useEffect(() => {
        if (!crypto_id){
            return;
        }

        const fetchCryptoData = async () => {
            setIsLoading(true);
            try{
                const response= await fetch (`https://api.coingecko.com/api/v3/coins/${crypto_id}?localization=false&tickers=false&developer_data=false&sparkline=false`);
                if (!response.ok){
                    throw new Error('Failed to fetch data');
                }
                const data = await response.json();
                setCryptoData(data);
                console.log(data);

            }
            catch(error: any){
                setError(error);
            }
            finally{
                setIsLoading(false);
        }
    }
    fetchCryptoData();

}, [crypto_id]);

    return { cryptoData, isLoading, error };
};



export default useCryptoData;