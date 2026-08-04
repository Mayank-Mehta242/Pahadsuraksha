import { useState } from "react";
import "../styles/dashboard.css";

function Dashboard() {
  const [routeData, setRouteData] = useState({
    source: "",
    destination: ""
  });

  const [weather, setWeather] = useState({
    condition: "--",
    rainfall: "--",
    humidity: "--",
    temperature: "--",
    windSpeed: "--"
  });

  const [prediction, setPrediction] = useState({
    risk: "--",
    recommendation: "--"
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleChange = (e) => {
    setRouteData({
      ...routeData,
      [e.target.name]: e.target.value
    });
  };

  const checkRoute = async () => {
    if (!routeData.source || !routeData.destination) {
      setError("Please enter both source and destination.");
      return;
    }

    setLoading(true);
    setError("");

    try {
      const token = localStorage.getItem("token");
      if (!token) {
        throw new Error("Please log in before checking the route.");
      }

      const response = await fetch("/api/prediction/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: token ? `Bearer ${token}` : ""
        },
        body: JSON.stringify({
          source: routeData.source.trim(),
          destination: routeData.destination.trim()
        })
      });

      const data = await response.json().catch(() => ({}));

      if (!response.ok) {
        throw new Error(data.message || `Unable to analyze route. (${response.status})`);
      }

      setWeather({
        condition: data.weather?.condition || "Unknown",
        rainfall: data.weather?.rainfall ?? "--",
        humidity: data.weather?.humidity ?? "--",
        temperature: data.weather?.temperature ?? "--",
        windSpeed: data.weather?.wind_speed ?? "--"
      });

      setPrediction({
        risk: data.prediction?.risk || "Unknown",
        recommendation: data.prediction?.recommendation || "No recommendation available."
      });
    } catch (err) {
      setError(err.message || "Unable to analyze route.");
      setPrediction({ risk: "--", recommendation: "--" });
    } finally {
      setLoading(false);
    }
  };



  return (

    <div className="dashboard">

      <h1>

        AI Landslide Travel Advisor

      </h1>

      <p>

        Check road safety between two locations in Uttarakhand.

      </p>



      {/* ===========================
              Route Input
      ============================ */}

      <div className="route-card">

        <h2>

          Route Information

        </h2>

        <div className="input-group">

          <label>

            Source

          </label>

          <input
            type="text"
            name="source"
            placeholder="Enter Source"
            value={routeData.source}
            onChange={handleChange}
          />

        </div>

        <div className="input-group">

          <label>

            Destination

          </label>

          <input
            type="text"
            name="destination"
            placeholder="Enter Destination"
            value={routeData.destination}
            onChange={handleChange}
          />

        </div>

        <button
          className="check-btn"
          onClick={checkRoute}
          disabled={loading}
        >
          {loading ? "Analyzing..." : "Check Route"}
        </button>

        {error && <p className="error-message">{error}</p>}

      </div>









      {/* ===========================
              AI Prediction
      ============================ */}

      <div className="prediction-card">

        <h2>

          AI Landslide Risk

        </h2>

        <div className="risk-box">
          {prediction.risk}
        </div>

      </div>





      {/* ===========================
          Recommendation
      ============================ */}

      <div className="recommendation-card">

        <h2>

          Travel Recommendation

        </h2>

        <p>

          {prediction.recommendation}

        </p>

      </div>

    </div>

  );

}

export default Dashboard;