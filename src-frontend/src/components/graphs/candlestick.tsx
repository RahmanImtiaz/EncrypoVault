import { useState, useEffect } from 'react';
import Chart from 'react-apexcharts';
import { ApexOptions } from 'apexcharts';
import {Socket} from 'socket.io-client';

interface CandlestickProps {
  crypto_id: string;
  time_range: number | string;
}

interface DataPoint {
  x: Date;
  y: number[];
}

const Candlestick: React.FC<CandlestickProps> = ({ crypto_id, time_range }) => {
  const [series, setSeries] = useState<{ data: DataPoint[] }[]>([]);
  const [minDate, setMinDate] = useState<number | null>(null);
  const [maxDate, setMaxDate] = useState<number | null>(null);
  const savedTheme = localStorage.getItem('theme');

  useEffect(() => {
    async function fetchData() {
      try {
        const socket = (await window.api.getCryptoSocket()) as Socket;
  

        socket.emit("message", {
          command: "proxy_data",
          type: "candlestick",
          coin_id: crypto_id,
          days: time_range,
        });
  
        const handle_response = (socketData: number[][]) => {
          console.log("Received candlestick data via socket:", socketData);
  

          const formattedData: DataPoint[] = socketData.map((entry) => ({
            x: new Date(entry[0]),
            y: [entry[1], entry[2], entry[3], entry[4]],
          }));
  
          const dates = formattedData.map((entry) => entry.x.getTime());
          const computedMinDate = Math.min(...dates);
          const computedMaxDate = Math.max(...dates);
  

          setSeries([{ data: formattedData }]);
          setMinDate(computedMinDate);
          setMaxDate(computedMaxDate);
        };
  

        socket.on("candlestick_response", handle_response);
  

        return () => {
          socket.off("candlestick_response", handle_response);
        };
      } catch (error) {
        console.error("Error fetching candlestick data:", error);
      }
    }
  
    fetchData();
  }, [crypto_id, time_range]);
  


  const options: ApexOptions = {
    chart: {
      type: 'candlestick',
      height: 350,
      background: savedTheme === 'dark' ? '#121212' : '#ffffff',
      events: {
        beforeZoom: function (_, { xaxis }) {
          // Ensure that minDate and maxDate are set
          if (minDate === null || maxDate === null) {
            return {};
          }

          let newMin = Math.max(xaxis.min, minDate);
          let newMax = Math.min(xaxis.max, maxDate);
          let minZoomRange: number = 0; // NOTE: The original logic uses an uninitialized variable

          if (minZoomRange <= 2) {
            minZoomRange = 30 * 60 * 1000;
          } else if (minZoomRange <= 30) {
            minZoomRange = 4 * 60 * 60 * 1000;
          } else {
            minZoomRange = 24 * 60 * 60 * 1000 * 4;
          }

          if (newMax - newMin < minZoomRange) {
            const midPoint = (newMin + newMax) / 2;
            newMin = Math.max(midPoint - minZoomRange / 2, minDate);
            newMax = Math.min(midPoint + minZoomRange / 2, maxDate);
          }

          return {
            xaxis: {
              min: newMin,
              max: newMax,
            },
          };
        },
      },
    },
    title: {
      text: 'Candlestick Chart',
      align: 'left',
      style: {
        color: savedTheme === 'dark' ? '#ffffff' : '#000000',
      },
    },
    xaxis: {
      type: 'datetime',
      min: minDate ?? undefined,
      max: maxDate ?? undefined,
      labels: {
        style: {
          colors: savedTheme === 'dark' ? '#ffffff' : '#000000',
        },
      },
    },
    yaxis: {
      tooltip: {
        enabled: true,
      },
      labels: {
        style: {
          colors: savedTheme === 'dark' ? '#ffffff' : '#000000',
        },
      },
    },
    grid: {
      borderColor: savedTheme === 'dark' ? '#333' : '#e0e0e0',
    },
    tooltip: {
      theme: savedTheme === 'dark' ? 'dark' : 'light',
      shared: false,
      y: {
        formatter: function (val: number) {
          return val.toFixed(2);
        },
      },
    },
    plotOptions: {
      candlestick: {
        colors: {
          upward: '#00E396',
          downward: '#FF4560',
        },
      },
    }
  };

  return (
    <div>
      <Chart options={options} series={series} type="candlestick" height={500} />
    </div>
  );
};

export default Candlestick;
