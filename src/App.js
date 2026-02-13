import React, { useEffect, useState } from "react";

function App() {
  const [data, setData] = useState([]);
  const [pumpStatus, setPumpStatus] = useState("OFF");

  const fetchData = () => {
    fetch("http://localhost:5000/data")
      .then(res => res.json())
      .then(data => setData(data));
  };

  const fetchStatus = () => {
    fetch("http://localhost:5000/status")
      .then(res => res.json())
      .then(data => setPumpStatus(data.pump_status));
  };

  useEffect(() => {
    fetchData();
    fetchStatus();
    const interval = setInterval(() => {
      fetchData();
      fetchStatus();
    }, 3000);
    return () => clearInterval(interval);
  }, []);

  const controlPump = (action) => {
    fetch("http://localhost:5000/control", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ action })
    });
  };

  return (
    <div style={{ padding: "20px" }}>
      <h1>🌱 Smart Farming Dashboard</h1>

      <h2>Pump Status: {pumpStatus}</h2>

      <button onClick={() => controlPump("ON")}>Turn ON</button>
      <button onClick={() => controlPump("OFF")}>Turn OFF</button>

      <h2>Sensor Data</h2>
      {data.map((item, index) => (
        <div key={index}>
          Moisture: {item.moisture} | Temp: {item.temperature} | Pump: {item.pump_status}
        </div>
      ))}
    </div>
  );
}

export default App;
