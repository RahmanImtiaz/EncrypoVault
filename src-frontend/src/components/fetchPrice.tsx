import { useState, useEffect } from "react";
import { Socket } from "socket.io-client";

interface PriceData {
  [key: string]: string | number;
}

interface useCryptoPriceResult {
  priceData: PriceData | null;
}

const useCryptoPrice = (): useCryptoPriceResult => {
    const [priceData, setPriceData] = useState<PriceData | null>(null);


  
    useEffect(() => {
      let socket: Socket | null = null;
  
      const fetchPriceData = async () => {
        try {
          socket = await window.api.getCryptoSocket() as Socket;
          
          socket.on("price_cache", (data: PriceData) => {
            setPriceData(data);

          });
  
          socket.emit("message", {
            command: "get_price"
          });
  
        } catch (error) {
            console.error("Error fetching price data:", error);
            const errorMessage = error instanceof Error ? error : new Error("An unknown error occurred");
            console.error(errorMessage);
            setPriceData(null);
        }
      };
  
      fetchPriceData(); // Initial fetch
  
      const interval = setInterval(fetchPriceData, 30000); // Poll every 60 seconds
  
      return () => {
        if (socket) {
          socket.off("price_cache"); // Clean up socket listener
        }
        clearInterval(interval); // Clear interval on unmount
      };
    }, []);
  
    return { priceData };
  };

export default useCryptoPrice;