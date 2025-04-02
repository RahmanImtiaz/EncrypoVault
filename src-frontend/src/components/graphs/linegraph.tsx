import React, { useState, useEffect } from 'react';
import Chart from 'react-apexcharts';
import { ApexOptions } from 'apexcharts';
import {Socket} from 'socket.io-client';

interface LineGraphProps {
  crypto_id: string;
  time_range: number;
}

interface PriceData {
  x: Date;
  y: number;
}

interface SeriesData {
  name: string;
  data: PriceData[];
}

interface socket_response{
  prices : number[][];
  market_caps : number[][];
  total_volumes : number[][];
}

const LineGraph: React.FC<LineGraphProps> = ({ crypto_id, time_range }) => {
  const [series, setSeries] = useState<SeriesData[]>([]);
  const [minDate, setMinDate] = useState<number | null>(null);
  const [maxDate, setMaxDate] = useState<number | null>(null);

  useEffect(() => {
    async function fetchData() {
      try {
        const socket = await window.api.getCryptoSocket() as Socket;
        console.log("Connecting to socket...");
        socket.emit("message", {
          command: "proxy_data",
          type: "linegraph",
          coin_id: crypto_id,
          days: time_range,
        });
        
        const handle_response = (socket_data: socket_response) => {
          console.log("Received line graph data via socket:", socket_data);

          const formattedData: PriceData[] = socket_data.prices.map((entry) => ({
            x: new Date(entry[0]),
            y: entry[1],
          }));

          const dates = formattedData.map((entry) => entry.x.getTime());
          const computedMinDate = Math.min(...dates);
          const computedMaxDate = Math.max(...dates);

          setSeries([{ name: 'Price', data: formattedData }]);
          setMinDate(computedMinDate);
          setMaxDate(computedMaxDate);
        };

        socket.on("linegraph_response", handle_response);
        return () => {
          socket.off("linegraph_response", handle_response);
        };

      } catch (error) {
        console.error("Error fetching data:", error);
      }
    }
    fetchData();
  }, [crypto_id, time_range]);

  const determineMinZoomRange = () => {
    if (time_range <= 1) {
      return 5 * 60 * 1000;
    } else if (time_range <= 90) {
      return 60 * 60 * 1000;
    } else {
      return 24 * 60 * 60 * 1000;
    }
  };

  const minZoomRange = determineMinZoomRange();

  const options: ApexOptions = {
    chart: {
      type: 'area',
      height: 350,
      zoom: {
        type: 'x',
        enabled: true,
        autoScaleYaxis: true,
      },
      toolbar: {
        autoSelected: 'zoom',
      },
      events: {
        beforeZoom: function (_: any, { xaxis }: { xaxis: { min: number; max: number } }) {
          let newMin = Math.max(xaxis.min, minDate || 0);
          let newMax = Math.min(xaxis.max, maxDate || Infinity);

          if (newMax - newMin < minZoomRange) {
            const midPoint = (newMin + newMax) / 2;
            newMin = Math.max(midPoint - minZoomRange / 2, minDate || 0);
            newMax = Math.min(midPoint + minZoomRange / 2, maxDate || Infinity);
          }

          return {
            xaxis: {
              min: newMin,
              max: newMax,
            },
          };
        },
      },
      background: '#121212',
    },
    dataLabels: {
      enabled: false,
    },
    markers: {
      size: 0,
    },
    title: {
      text: 'Price Movement',
      align: 'left',
      style: {
        color: '#ffffff', 
      },
    },
    fill: {
      type: 'gradient',
      gradient: {
        shadeIntensity: 1,
        inverseColors: false,
        opacityFrom: 0.5,
        opacityTo: 0,
        stops: [0, 90, 100],
      },
    },
    yaxis: {
      labels: {
        style: {
          colors: '#ffffff', 
        },
        formatter: function (val : number) {
          return val.toFixed(2);
        },
      },
      title: {
        text: 'Price (GBP)',
        style: {
          color: '#ffffff',
        },
      },
    },
    xaxis: {
      type: 'datetime',
      min: minDate || undefined,
      max: maxDate || undefined,
      labels: {
        style: {
          colors: '#ffffff', 
        },
      },
    },
    tooltip: {
      theme: 'dark',
      shared: false,
      y: {
        formatter: function (val: number) {
          return val.toFixed(2);
        },
      },
    },
    grid: {
      borderColor: '#333',
    },
    plotOptions: {
      area: {},
    },
    colors: ['#00E396'], 
  };

  return (
    <div id="chart">
      <Chart options={options} series={series} type="area" height={350} />
    </div>
  );
};

export default LineGraph;
