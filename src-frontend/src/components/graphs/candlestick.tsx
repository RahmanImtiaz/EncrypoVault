import { useState, useEffect } from 'react';
import Chart from 'react-apexcharts';
import { ApexOptions } from 'apexcharts';

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

  useEffect(() => {
    const fetchData = async () => {
      try {
        const options = {
          method: 'GET',
          headers: {
            accept: 'application/json',
            'x-cg-demo-api-key': 'CG-E46h8ehSNZFLW8b3zrv1xzyP',
          },
        };

        const response = await fetch(`https://api.coingecko.com/api/v3/coins/${crypto_id}/ohlc?vs_currency=gbp&days=${time_range}`, options);
        const data: number[][] = await response.json();

        const formattedData: DataPoint[] = data.map(entry => ({
          x: new Date(entry[0]),
          y: [entry[1], entry[2], entry[3], entry[4]],
        }));

        const dates = formattedData.map(entry => entry.x.getTime());
        const computedMinDate = Math.min(...dates);
        const computedMaxDate = Math.max(...dates);

        setSeries([{ data: formattedData }]);
        setMinDate(computedMinDate);
        setMaxDate(computedMaxDate);
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };

    fetchData();
  }, [crypto_id, time_range]);

  const options: ApexOptions = {
    chart: {
      type: 'candlestick',
      height: 350,
      background: '#121212',
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
        color: '#ffffff',
      },
    },
    xaxis: {
      type: 'datetime',
      min: minDate ?? undefined,
      max: maxDate ?? undefined,
      labels: {
        style: {
          colors: '#ffffff',
        },
      },
    },
    yaxis: {
      tooltip: {
        enabled: true,
      },
      labels: {
        style: {
          colors: '#ffffff',
        },
      },
    },
    grid: {
      borderColor: '#333',
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
