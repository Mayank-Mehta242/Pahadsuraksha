import { useEffect, useState } from "react";
import { Line, Bar } from "react-chartjs-2";
import { Droplets, Thermometer, Wind, CloudRain } from "lucide-react";
import Card from "../components/Card.jsx";
import LoadingSpinner from "../components/LoadingSpinner.jsx";
import { weatherService } from "../services/weatherService.js";
import { baseChartOptions } from "../components/charts/chartSetup.js";
import { UTTARAKHAND_CENTER } from "../utils/constants.js";

export default function WeatherAnalyticsPage() {
  const [weather, setWeather] = useState(null);

  useEffect(() => {
    weatherService.getWeather(UTTARAKHAND_CENTER.lat, UTTARAKHAND_CENTER.lng).then(setWeather);
  }, []);

  if (!weather) return <LoadingSpinner label="Loading weather data" />;

  const labels = weather.forecast.map((f) => f.day);

  const rainfallData = {
    labels,
    datasets: [
      {
        label: "Rainfall (mm)",
        data: weather.forecast.map((f) => f.rainMm),
        borderColor: "#2A9D6B",
        backgroundColor: "rgba(42,157,107,0.2)",
        fill: true,
        tension: 0.35,
      },
    ],
  };

  const tempData = {
    labels,
    datasets: [
      {
        label: "Temperature (°C)",
        data: weather.forecast.map((f) => f.tempC),
        borderColor: "#3B82F6",
        backgroundColor: "rgba(59,130,246,0.2)",
        fill: true,
        tension: 0.35,
      },
    ],
  };

  const humidityData = {
    labels,
    datasets: [
      {
        label: "Humidity (%)",
        data: weather.forecast.map((f) => f.humidityPct),
        backgroundColor: "#E0B324",
        borderRadius: 6,
      },
    ],
  };

  return (
    <div>
      <p>Weather Analytics</p>
      <h1 className="text-2xl font-display font-bold text-white mb-6">{weather.location} — 7-day outlook</h1>

      <div className="grid sm:grid-cols-4 gap-4 mb-6">
        <Metric icon={CloudRain} label="Condition" value={weather.condition} />
        <Metric icon={Thermometer} label="Temperature" value={`${weather.temperatureC}°C`} />
        <Metric icon={Droplets} label="Humidity" value={`${weather.humidityPct}%`} />
        <Metric icon={Wind} label="Wind" value={`${weather.windKmh} km/h`} />
      </div>

      <div className="grid lg:grid-cols-2 gap-6">
        <Card title="Rainfall forecast">
          <div className="h-64">
            <Line data={rainfallData} options={baseChartOptions} />
          </div>
        </Card>
        <Card title="Temperature forecast">
          <div className="h-64">
            <Line data={tempData} options={baseChartOptions} />
          </div>
        </Card>
        <Card title="Humidity forecast" className="lg:col-span-2">
          <div className="h-64">
            <Bar data={humidityData} options={baseChartOptions} />
          </div>
        </Card>
      </div>
    </div>
  );
}

function Metric({ icon: Icon, label, value }) {
  return (
    <div className="glass-panel p-4 flex items-center gap-3">
      <Icon className="h-5 w-5 text-forest-500 shrink-0" />
      <div>
        <p className="text-xs text-slate-300">{label}</p>
        <p className="text-sm font-mono text-white">{value}</p>
      </div>
    </div>
  );
}
