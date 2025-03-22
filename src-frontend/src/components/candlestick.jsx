import { useState, useEffect } from 'react';
import Chart from 'react-apexcharts';

const Candlestick = ({crypto_id, time_range}) => {
  const [series, setSeries] = useState([]);
  const [minDate, setMinDate] = useState(null);
  const [maxDate, setMaxDate] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {

        const options = {
            method: 'GET',
            headers: {
              accept: 'application/json',
              'x-cg-demo-api-key': '	CG-E46h8ehSNZFLW8b3zrv1xzyP'
            }
        };
          


        const response = await fetch(`https://api.coingecko.com/api/v3/coins/${crypto_id}/ohlc?vs_currency=gbp&days=${time_range}`, options);
        const data = await response.json();


        const formattedData = data.map(entry => ({
          x: new Date(entry[0]),
          y: [entry[1], entry[2], entry[3], entry[4]]
        }));


        const dates = formattedData.map(entry => entry.x.getTime());
        const minDate = Math.min(...dates);
        const maxDate = Math.max(...dates);

        setSeries([{ data: formattedData }]);
        setMinDate(minDate);
        setMaxDate(maxDate);
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };

    fetchData();
  }, [crypto_id, time_range]);

  const options = {
    chart: {
      type: 'candlestick',
      height: 350,
      events: {
        beforeZoom: function(chartContext, { xaxis }) {
          let newMin = Math.max(xaxis.min, minDate);
          let newMax = Math.min(xaxis.max, maxDate);
          let minZoomRange;

          if (minZoomRange <=2){
            minZoomRange= 30 * 60 * 1000;
          }
          else if (minZoomRange <= 30){
            minZoomRange= 4 * 60 * 60 * 1000;
          } else{
            minZoomRange= 24 * 60 * 60 * 1000 * 4;
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
    xaxis: {
      type: 'datetime',
      min: minDate,
      max: maxDate,
    },
    yaxis: {
      tooltip: {
        enabled: true,
      },
    },
    title: {
      text: 'Candlestick Chart',
      align: 'left',
    },
  };

  return (
    <div>
      <Chart options={options} series={series} type="candlestick" height={500} />
    </div>
  );
};

export default Candlestick;
