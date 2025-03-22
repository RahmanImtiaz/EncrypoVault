import React, { useState, useEffect } from 'react';
import Chart from 'react-apexcharts';

const LineGraph = ({ crypto_id, time_range }) => {
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
          
        const response = await fetch(`https://api.coingecko.com/api/v3/coins/${crypto_id}/market_chart?vs_currency=gbp&days=${time_range}`, options);
        const data = await response.json();

        const prices = data.prices.map(price => ({
          x: new Date(price[0]),
          y: price[1],
        }));

        const dates = prices.map(entry => entry.x.getTime());
        const minDate = Math.min(...dates);
        const maxDate = Math.max(...dates);

        setSeries([{ name: 'Price', data: prices }]);
        setMinDate(minDate);
        setMaxDate(maxDate);
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };

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

  const options = {
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
        beforeZoom: function (chartContext, { xaxis }) {
          let newMin = Math.max(xaxis.min, minDate);
          let newMax = Math.min(xaxis.max, maxDate);

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
    dataLabels: {
      enabled: false,
    },
    markers: {
      size: 0,
    },
    title: {
      text: 'Price Movement',
      align: 'left',
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
        formatter: function (val) {
          return val.toFixed(2);
        },
      },
      title: {
        text: 'Price (GBP)',
      },
    },
    xaxis: {
      type: 'datetime',
      min: minDate,
      max: maxDate,
    },
    tooltip: {
      shared: false,
      y: {
        formatter: function (val) {
          return val.toFixed(2);
        },
      },
    },
  };

  return (
    <div id="chart">
      <Chart options={options} series={series} type="area" height={350} />
    </div>
  );
};

export default LineGraph;
