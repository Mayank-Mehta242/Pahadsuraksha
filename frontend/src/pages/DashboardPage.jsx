import { useEffect, useState } from "react";
import { Search, LocateFixed, Droplets, Thermometer, Wind, Mountain as MountainIcon, History } from "lucide-react";
import MapView from "../components/MapView.jsx";
import Card from "../components/Card.jsx";
import RiskBadge from "../components/RiskBadge.jsx";
import LoadingSpinner from "../components/LoadingSpinner.jsx";
import { districtService } from "../services/districtService.js";
import { weatherService } from "../services/weatherService.js";
import { useGeolocation } from "../hooks/useGeolocation.js";

export default function DashboardPage() {
  const [districts, setDistricts] = useState([]);
  const [selected, setSelected] = useState(null);
  const [weather, setWeather] = useState(null);
  const [weatherError, setWeatherError] = useState("");
  const [weatherRequest, setWeatherRequest] = useState(0);
  const [search, setSearch] = useState("");
  const { position, error: locationError, locate, locating } = useGeolocation();

  useEffect(() => {
    districtService.list().then((list) => {
      setDistricts(list);
      setSelected(list[0]);
    });
  }, []);

  useEffect(() => {
    if (!selected) return;
    setWeather(null);
    setWeatherError("");
    weatherService
      .getWeather(selected.lat, selected.lng)
      .then(setWeather)
      .catch(() => setWeatherError("Weather conditions are unavailable right now."));
  }, [selected, weatherRequest]);

  useEffect(() => {
    if (!position) return;
    setSelected((prev) => prev ?? districts[0]);
  }, [position, districts]);

  function handleMapClick(latlng) {
    // Find nearest district to clicked point
    let nearest = districts[0];
    let best = Infinity;
    for (const d of districts) {
      const dist = Math.hypot(d.lat - latlng.lat, d.lng - latlng.lng);
      if (dist < best) {
        best = dist;
        nearest = d;
      }
    }
    setSelected(nearest);
  }

  const filtered = districts.filter((d) => d.name.toLowerCase().includes(search.toLowerCase()));

  return (
    <div>
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-6">
        <div>
          <h1 className="text-2xl font-bold text-white">Risk Map</h1>
          <p className="text-slate-200 text-sm mt-1">Click on a district to see conditions and risk level</p>
        </div>
        <div className="flex flex-wrap sm:flex-nowrap gap-2 w-full sm:w-auto">
          <div className="relative flex-1 sm:flex-none">
            <Search className="h-4 w-4 text-slate-500 absolute left-3 top-1/2 -translate-y-1/2" />
            <input
              className="input-field pl-9 w-full sm:w-56"
              placeholder="Search district…"
              value={search}
              onChange={(e) => setSearch(e.target.value)}
            />
          </div>
          <button onClick={locate} className="btn-secondary whitespace-nowrap">
            <LocateFixed className="h-4 w-4" />
            {locating ? "Locating…" : "My Location"}
          </button>
        </div>
      </div>

      <div className="grid lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 space-y-3">
          {districts.length === 0 ? (
            <LoadingSpinner label="Loading district data" />
          ) : (
            <MapView
              districts={filtered}
              onSelectDistrict={setSelected}
              onMapClick={handleMapClick}
              userPosition={position}
            />
          )}
          <p className="text-xs text-slate-600">
            Click anywhere on the map to preview that area's nearest risk reading, or search a district by name.
          </p>
          {locationError && <p className="text-xs text-risk-high">{locationError}</p>}
        </div>

        <div className="space-y-4">
          {selected && (
            <Card title={selected.name}>
              <div className="mb-3">
                <RiskBadge level={selected.risk} size="lg" />
              </div>
              {weather ? (
                <div className="grid grid-cols-2 gap-3">
                  <Metric icon={Droplets} label="Rainfall" value={`${weather.rainfallMm} mm`} />
                  <Metric icon={Thermometer} label="Temp" value={`${weather.temperatureC}°C`} />
                  <Metric icon={Wind} label="Wind" value={`${weather.windKmh} km/h`} />
                  <Metric icon={MountainIcon} label="Elevation" value={`${weather.elevationM} m`} />
                  <Metric icon={Droplets} label="Humidity" value={`${weather.humidityPct}%`} />
                  <Metric icon={History} label="Incidents" value={selected.incidents} />
                </div>
              ) : weatherError ? (
                <div className="space-y-3">
                  <p className="text-sm text-slate-200">{weatherError}</p>
                  <button
                    type="button"
                    onClick={() => setWeatherRequest((request) => request + 1)}
                    className="btn-secondary text-sm"
                  >
                    Try again
                  </button>
                </div>
              ) : (
                <LoadingSpinner label="Loading conditions" />
              )}
            </Card>
          )}

          <Card title="Risk Levels">
            <div className="space-y-2 text-sm">
              <LegendRow color="bg-risk-low" label="Low — safe" />
              <LegendRow color="bg-risk-medium" label="Medium — caution" />
              <LegendRow color="bg-risk-high" label="High — avoid" />
              <LegendRow color="bg-risk-extreme" label="Very High — do not travel" />
            </div>
          </Card>
        </div>
      </div>
    </div>
  );
}

function Metric({ icon: Icon, label, value }) {
  return (
    <div>
      <p className="text-xs text-slate-300 mb-0.5">{label}</p>
      <p className="text-sm font-medium text-white">{value}</p>
    </div>
  );
}

function LegendRow({ color, label }) {
  return (
    <div className="flex items-center gap-2">
      <span className={`h-2 w-2 rounded-full ${color}`} />
      <span className="text-slate-200">{label}</span>
    </div>
  );
}
