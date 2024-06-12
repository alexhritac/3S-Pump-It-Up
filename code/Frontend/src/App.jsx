import 'bootstrap/dist/css/bootstrap.css';
import React, { useEffect, useState } from "react";
import axios from "axios";
import { Chart as ChartJS, defaults } from "chart.js/auto";
import { Line } from "react-chartjs-2";
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";
import moment from "moment";

import "./App.css";

defaults.maintainAspectRatio = false;
defaults.responsive = true;
defaults.plugins.title.display = true;
defaults.plugins.title.align = "center";
defaults.plugins.title.font.size = 20;
defaults.plugins.title.color = "black";

export const App = () => {
  const [sensorData, setSensorData] = useState({});
  const [realTime, setRealTime] = useState(true);
  const [startDate, setStartDate] = useState(() => {
    const today = new Date();
    today.setHours(today.getHours() - 24);
    return today;
  });
  const [endDate, setEndDate] = useState(new Date());

  useEffect(() => {
    const fetchData = async () => {
      try {
        const url = realTime ? "http://localhost:5000/sensor_data_rt" : "http://localhost:5000/sensor_data_hs";
        const response = await axios.get(url);
        console.log(response.data)
        setSensorData(response.data);
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    };

    fetchData();

    const interval = setInterval(fetchData, 1 * 60 * 1000);

    return () => clearInterval(interval); // Cleanup function to clear interval on unmount
  }, [realTime]);

  const handleDropdownChange = (event) => {
    setRealTime(event.target.value === "Real-time");
  };

  const filterDataByDate = (data) => {
    return data.filter(entry => {
      const entryDate = moment(entry.date);
      return entryDate.isSameOrAfter(moment(startDate)) && entryDate.isSameOrBefore(moment(endDate));
    });
  };

  // Render date pickers only if historical data is selected
  const renderDatePickers = () => {
    if (!realTime) {
      return (
        <div className="d-flex justify-content-center align-items-center">
          <div className="d-flex flex-column mx-2">
            <label className="form-label">Start Date</label>
            <DatePicker
              selected={startDate}
              onChange={(date) => setStartDate(date)}
              showTimeSelect
              dateFormat="dd-MM-yyyy HH:mm"
              className="form-control"
            />
          </div>
          <div className="d-flex flex-column mx-2">
            <label className="form-label">End Date</label>
            <DatePicker
              selected={endDate}
              onChange={(date) => setEndDate(date)}
              showTimeSelect
              dateFormat="dd-MM-yyyy HH:mm"
              className="form-control"
            />
          </div>
        </div>
      );
    }
  };

  return (
    <>
      <h1 className='text-center pt-3'>Measurement Dashboard</h1>
      <div className="container">
        <div className="row gy-3 pt-3 pb-3 gx-3">
          <div className="col-12 mb-3">
            <div className="d-flex justify-content-center align-items-center">
              <select onChange={handleDropdownChange} className="form-select form-select-lg mb-3">
                <option>Real-time</option>
                <option>Historical</option>
              </select>
            </div>
          </div>
          {renderDatePickers()}
          {Object.keys(sensorData).map(sensor => (
            <div className="col-lg-6 col-12" key={sensor}>
              <div className='dataCardWrapper'>
                <div className='dataCard'>
                  <Line
                    data={{
                      labels: filterDataByDate(sensorData[sensor]).map(data => new Date(data.date).toLocaleString('nl-NL')),
                      datasets: [
                        {
                          label: sensor,
                          data: filterDataByDate(sensorData[sensor]).map(data => data.value),
                          backgroundColor: "#064FF0",
                          borderColor: "#064FF0",
                        },
                      ],
                    }}
                    options={{
                      scales: {
                        y: {
                          title: {
                            display: true,
                            text: 'Measured Value'
                          }
                        },
                        x: {
                          title: {
                            display: true,
                            text: 'Date'
                          },
                          ticks: {
                            autoSkip: true,
                            maxTicksLimit: 100
                          }
                        }
                      },
                      elements: {
                        line: {
                          tension: 0.5,
                        },
                      },
                      plugins: {
                        title: {
                          text: sensor,
                        },
                      },
                    }}
                  />
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </>
  );
};

export default App;
