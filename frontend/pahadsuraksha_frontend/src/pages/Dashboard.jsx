import { useState } from "react";
import "../styles/dashboard.css";

function Dashboard() {

  /* ==========================================================
      USER INPUT
      Source & Destination
  ========================================================== */

  const [routeData, setRouteData] = useState({
    source: "",
    destination: ""
  });

  /* ==========================================================
      WEATHER DATA
      Replace this with OpenWeather API response later
  ========================================================== */

  const [weather, setWeather] = useState({
    condition: "--",
    rainfall: "--",
    humidity: "--",
    temperature: "--",
    windSpeed: "--"
  });

  /* ==========================================================
      AI PREDICTION
      Replace this with Flask API response
  ========================================================== */

  const [prediction, setPrediction] = useState({
    risk: "--",
    recommendation: "--"
  });

  const handleChange = (e) => {
    setRouteData({
      ...routeData,
      [e.target.name]: e.target.value
    });
  };

  const checkRoute = async () => {

    /* ==========================================================
        STEP 1
        Use Geocoding API
        Convert Source & Destination into coordinates

        Example:
        Source -> Latitude, Longitude
        Destination -> Latitude, Longitude
    ========================================================== */


    /* ==========================================================
        STEP 2
        Use OpenWeather API

        Fetch weather for Source
        OR multiple points on the route.

        Example Endpoint

        /weather?lat=...&lon=...

        Update

        setWeather(...)
    ========================================================== */


    /* ==========================================================
        STEP 3

        Send weather + route information to Flask

        POST /predict

        {
            source,
            destination,
            rainfall,
            humidity,
            temperature,
            windSpeed
        }

        Response

        {
            risk:"Medium",
            recommendation:"Travel with Caution"
        }

        Update

        setPrediction(...)
    ========================================================== */

    console.log("API Integration Here");

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
        >

          Check Route

        </button>

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