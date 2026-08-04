import { useState } from "react";
import "../styles/weather.css";

function Weather() {

  /* ==========================================================
      USER SEARCH
  ========================================================== */

  const [location, setLocation] = useState("Tehri Garhwal");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  /* ==========================================================
      CURRENT WEATHER
      Replace these values using OpenWeather API
  ========================================================== */

  const [weather, setWeather] = useState({

    city: "Tehri Garhwal",

    condition: "Partly Cloudy",

    icon: "🌤",

    temperature: "24°C",

    feelsLike: "26°C",

    humidity: "82%",

    rainfall: "12 mm",

    windSpeed: "18 km/h",

    visibility: "6 km",

    pressure: "1012 hPa",

    uvIndex: "5",

    updated: "2:45 PM"

  });

  /* ==========================================================
      ROAD SAFETY STATUS

      This value should come from your Flask AI backend.
  ========================================================== */

  const [roadStatus, setRoadStatus] = useState({

    level: "🟡 Moderate",

    color: "#F9A825"

  });

  /* ==========================================================
      WEATHER ALERTS

      Replace using Weather API
  ========================================================== */

  const [alerts, setAlerts] = useState([
    "Heavy Rain Warning",
    "Strong Winds",
    "Thunderstorm Alert"
  ]);

  /* ==========================================================
      HOURLY FORECAST

      Replace using OpenWeather Forecast API
  ========================================================== */

  const [hourlyForecast, setHourlyForecast] = useState([
    { time: "1 PM", icon: "🌤", temp: "24°C" },
    { time: "2 PM", icon: "🌦", temp: "23°C" },
    { time: "3 PM", icon: "🌧", temp: "22°C" },
    { time: "4 PM", icon: "🌧", temp: "21°C" },
    { time: "5 PM", icon: "⛈", temp: "20°C" }
  ]);

  /* ==========================================================
      WEEKLY FORECAST

      Replace using OpenWeather Daily API
  ========================================================== */

  const [weeklyForecast, setWeeklyForecast] = useState([
    { day: "Sun", icon: "🌤", temp: "25°C" },
    { day: "Mon", icon: "🌦", temp: "24°C" },
    { day: "Tue", icon: "🌧", temp: "22°C" },
    { day: "Wed", icon: "⛈", temp: "20°C" },
    { day: "Thu", icon: "🌤", temp: "24°C" },
    { day: "Fri", icon: "🌥", temp: "23°C" },
    { day: "Sat", icon: "🌤", temp: "25°C" }
  ]);

  /* ==========================================================
      SEARCH WEATHER

      API FLOW

      React
          ↓
      Flask Backend
          ↓
      Geocoding API
          ↓
      OpenWeather API
          ↓
      AI Landslide Model
          ↓
      React UI
  ========================================================== */

  const searchWeather = async () => {
    if (!location.trim()) {
      setError("Please enter a city or location.");
      return;
    }

    setLoading(true);
    setError("");

    try {
      const response = await fetch(`/api/weather/?city=${encodeURIComponent(location)}`);
      const data = await response.json().catch(() => ({}));

      if (!response.ok) {
        throw new Error(data.message || "Unable to fetch weather data.");
      }

      setWeather({
        city: data.city || location,
        condition: data.description || data.condition || "Unknown",
        icon: data.icon ? `🌤` : "🌤",
        temperature: `${Math.round(data.temperature)}°C`,
        feelsLike: `${Math.round(data.feelsLike)}°C`,
        humidity: `${data.humidity}%`,
        rainfall: `${data.rainfall} mm`,
        windSpeed: `${data.windSpeed} km/h`,
        visibility: `${data.visibility} m`,
        pressure: `${data.pressure} hPa`,
        uvIndex: "5",
        updated: new Date().toLocaleTimeString([], { hour: "numeric", minute: "2-digit" })
      });

      setRoadStatus({
        level: data.roadStatus?.level || "Safe",
        color: data.roadStatus?.color === "red" ? "#d32f2f" : data.roadStatus?.color === "orange" ? "#f57c00" : data.roadStatus?.color === "yellow" ? "#fbc02d" : "#2e7d32"
      });

      setAlerts(data.alerts || []);
      setHourlyForecast((data.hourlyForecast || []).slice(0, 5).map((item) => ({
        time: new Date(item.time).toLocaleTimeString([], { hour: "numeric", minute: "2-digit" }),
        icon: "🌤",
        temp: `${Math.round(item.temperature)}°C`
      })));
      setWeeklyForecast((data.weeklyForecast || []).slice(0, 7).map((item) => ({
        day: item.day || "Day",
        icon: "🌤",
        temp: `${Math.round(item.temperature)}°C`
      })));
    } catch (err) {
      setError(err.message || "Unable to fetch weather data.");
    } finally {
      setLoading(false);
    }
  };

  return (

    <div className="weather-page">

      {/* ================= HEADER ================= */}

      <div className="weather-header">

        <h1>

          Live Weather

        </h1>

        <p>

          AI Powered Weather & Road Safety

        </p>

      </div>

      {/* ================= SEARCH ================= */}

      <div className="search-card">

        <input
          type="text"
          placeholder="Search City / Location"
          value={location}
          onChange={(e) => setLocation(e.target.value)}
        />

        <button onClick={searchWeather} disabled={loading}>
          {loading ? "Loading..." : "Search"}
        </button>

        {error && <p className="error-message">{error}</p>}

      </div>

      {/* ====================================================
                  FIRST ROW
      ==================================================== */}

      <div className="top-row">

        {/* LEFT SIDE */}

        <div className="left-column">

          <div className="current-weather">

            <h2>

              {weather.city}

            </h2>

            <div className="weather-icon">

              {weather.icon}

            </div>

            <h3>

              {weather.condition}

            </h3>

            <h1>

              {weather.temperature}

            </h1>

            <p>

              Feels Like : {weather.feelsLike}

            </p>

            <p>

              Last Updated : {weather.updated}

            </p>

          </div>

        </div>

        {/* RIGHT SIDE */}

        <div className="right-column">

          <div className="weather-details">

            <div className="detail-card">
              <h3>🌡 Temperature</h3>
              <p>{weather.temperature}</p>
            </div>

            <div className="detail-card">
              <h3>💧 Humidity</h3>
              <p>{weather.humidity}</p>
            </div>

            <div className="detail-card">
              <h3>🌧 Rainfall</h3>
              <p>{weather.rainfall}</p>
            </div>

            <div className="detail-card">
              <h3>💨 Wind Speed</h3>
              <p>{weather.windSpeed}</p>
            </div>

            <div className="detail-card">
              <h3>🌫 Visibility</h3>
              <p>{weather.visibility}</p>
            </div>

            <div className="detail-card">
              <h3>📈 Pressure</h3>
              <p>{weather.pressure}</p>
            </div>

            <div className="detail-card">
              <h3>☀ UV Index</h3>
              <p>{weather.uvIndex}</p>
            </div>

          </div>

        </div>

      </div>

      {/* ==========================================
                SECOND ROW
      =========================================== */}

      <div className="second-row">

        {/* Road Safety */}

        <div className="road-status">

          <h2>

            Road Safety Status

          </h2>

          <div
            className="status-box"
            style={{
              background: roadStatus.color
            }}
          >

            {roadStatus.level}

          </div>

          <p>

            AI evaluates rainfall, humidity,
            wind speed and terrain conditions
            to estimate travel safety.

          </p>

        </div>

        {/* AI Recommendation */}

        <div className="recommendation-section">

          <h2>

            AI Travel Recommendation

          </h2>

          <div className="recommendation-card">

            <div className="recommendation-status">

              🟡 Drive with Caution

            </div>

            <p>

              Moderate rainfall detected around
              Tehri Garhwal.

            </p>

            <ul>

              <li>

                ✔ Drive below 40 km/h

              </li>

              <li>

                ✔ Keep headlights ON

              </li>

              <li>

                ✔ Maintain safe distance

              </li>

              <li>

                ✔ Avoid landslide-prone routes

              </li>

            </ul>

          </div>

        </div>

      </div>

      {/* ==========================================
                THIRD ROW
                Hourly Forecast
      =========================================== */}

      <div className="hourly-section">

        <h2>

          Hourly Forecast

        </h2>

        <div className="hourly-container">

          {

            hourlyForecast.map((hour,index)=>(

              <div
                className="hour-card"
                key={index}
              >

                <h3>

                  {hour.time}

                </h3>

                <p>

                  {hour.icon}

                </p>

                <p>

                  {hour.temp}

                </p>

              </div>

            ))

          }

        </div>

      </div>
            {/* ==========================================
                FOURTH ROW
                Weekly Forecast
      =========================================== */}

      <div className="weekly-section">

        <h2>

          7 Day Forecast

        </h2>

        <div className="week-grid">

          {

            weeklyForecast.map((day,index)=>(

              <div
                className="day-card"
                key={index}
              >

                <h3>

                  {day.day}

                </h3>

                <p>

                  {day.icon}

                </p>

                <p>

                  {day.temp}

                </p>

              </div>

            ))

          }

        </div>

      </div>



      {/* ==========================================
                FIFTH ROW
                Weather Alerts
      =========================================== */}

      <div className="alerts-section">

        <h2>

          Weather Alerts

        </h2>

        <div className="alerts-list">

          {

            alerts.map((alert,index)=>(

              <div
                className="alert-card"
                key={index}
              >

                ⚠ {alert}

              </div>

            ))

          }

        </div>

      </div>



      {/* ==========================================

            BACKEND API FLOW

            React

                ↓

            Flask Backend

                ↓

            Geocoding API

                ↓

            OpenWeather API

                ↓

            AI Landslide Prediction Model

                ↓

            React UI

      ==========================================


      POST

      /weather

      {

          location

      }


      Backend Response


      {

          weather:{

              city,

              condition,

              icon,

              temperature,

              feelsLike,

              humidity,

              rainfall,

              windSpeed,

              visibility,

              pressure,

              uvIndex,

              updated

          },

          roadStatus:{

              level,

              color

          },

          hourlyForecast:[ ],

          weeklyForecast:[ ],

          alerts:[ ]

      }


      Update these states

      setWeather()

      setRoadStatus()

      setHourlyForecast()

      setWeeklyForecast()

      setAlerts()

      */}

    </div>

  );

}

export default Weather;