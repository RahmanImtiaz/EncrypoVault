import { useState, useEffect } from "react";


const UseCryptoData = (crypto_id) => {
    const[cryptoData, setCryptoData] = useState([]);
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
            catch(error){
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



export default UseCryptoData;