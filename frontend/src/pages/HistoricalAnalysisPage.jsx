import { useEffect, useState } from "react";
import { Bar, Line } from "react-chartjs-2";
import Card from "../components/Card.jsx";
import LoadingSpinner from "../components/LoadingSpinner.jsx";
import { districtService } from "../services/districtService.js";
import { baseChartOptions } from "../components/charts/chartSetup.js";

export default function HistoricalAnalysisPage() {
  const [data, setData] = useState(null);

  useEffect(() => {
    districtService.historical().then(setData);
  }, []);

  if (!data) return <LoadingSpinner label="Loading historical records" />;

  const monthlyData = {
    labels: data.monthly.map((m) => m.month),
    datasets: [
      {
        label: "Landslides reported",
        data: data.monthly.map((m) => m.count),
        backgroundColor: "#166944",
        borderRadius: 6,
      },
    ],
  };

  const yearlyData = {
    labels: data.yearly.map((y) => y.year),
    datasets: [
      {
        label: "Yearly total",
        data: data.yearly.map((y) => y.count),
        borderColor: "#2A9D6B",
        backgroundColor: "rgba(42,157,107,0.15)",
        fill: true,
        tension: 0.3,
      },
    ],
  };

  return (
    <div>
      <p>Historical Analysis</p>
      <h1 className="text-2xl font-display font-bold text-slate-900 mb-6">Landslide records, district-wise</h1>

      <div className="grid lg:grid-cols-2 gap-6 mb-6">
        <Card title="Monthly landslides (seasonal pattern)">
          <div className="h-64">
            <Bar data={monthlyData} options={baseChartOptions} />
          </div>
        </Card>
        <Card title="Yearly trend">
          <div className="h-64">
            <Line data={yearlyData} options={baseChartOptions} />
          </div>
        </Card>
      </div>

      <Card title="Top vulnerable districts">
        <ol className="space-y-3">
          {data.topVulnerable.map((d, i) => (
            <li key={d} className="flex items-center gap-3">
              <span className="h-7 w-7 rounded-full bg-forest-800/60 border border-forest-600/40 flex items-center justify-center text-xs font-mono text-forest-500 shrink-0">
                {i + 1}
              </span>
              <span className="text-sm text-slate-700">{d}</span>
            </li>
          ))}
        </ol>
        <p className="text-xs text-slate-500 mt-4">
          {/* TODO(BACKEND): replace with a real Leaflet heat-map layer sourced
              from GET /api/districts/historical once incident-level lat/lng
              density data is available. */}
          A geographic heat map of incident density will render here once point-level historical data is connected.
        </p>
      </Card>
    </div>
  );
}
