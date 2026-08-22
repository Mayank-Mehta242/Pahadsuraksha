import { useState } from "react";
import toast from "react-hot-toast";
import { Loader2 } from "lucide-react";
import Card from "../components/Card.jsx";
import RiskBadge from "../components/RiskBadge.jsx";
import { predictionService } from "../services/predictionService.js";

const FIELDS = [
  { key: "rainfall", label: "Rainfall (mm, last 48h)", placeholder: "e.g. 45" },
  { key: "humidity", label: "Humidity (%)", placeholder: "e.g. 78" },
  { key: "temperature", label: "Temperature (°C)", placeholder: "e.g. 16" },
  { key: "elevation", label: "Elevation (m)", placeholder: "e.g. 1800" },
  { key: "slope", label: "Slope (°)", placeholder: "e.g. 38" },
  { key: "historicalIncidents", label: "Historical incidents nearby", placeholder: "e.g. 4" },
];

export default function PredictionPage() {
  const [form, setForm] = useState({});
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);

  async function handleSubmit(e) {
    e.preventDefault();
    setLoading(true);
    setResult(null);
    try {
      const output = await predictionService.predict(form);
      setResult(output);
    } catch (err) {
      toast.error("Could not get risk estimate. Please try again.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div>
      <h1 className="text-2xl font-bold text-slate-900 mb-2">Check Travel Risk</h1>
      <p className="text-slate-700 mb-6">
        Enter the conditions for your location to see an estimated landslide risk level.
      </p>

      <div className="grid lg:grid-cols-2 gap-6">
        <Card title="Location Details">
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="grid sm:grid-cols-2 gap-4">
              {FIELDS.map((f) => (
                <div key={f.key}>
                  <label className="text-sm text-slate-700 mb-1.5 block">{f.label}</label>
                  <input
                    type="number"
                    step="any"
                    required
                    className="input-field"
                    placeholder={f.placeholder}
                    value={form[f.key] ?? ""}
                    onChange={(e) => setForm({ ...form, [f.key]: e.target.value })}
                  />
                </div>
              ))}
            </div>
            <button type="submit" disabled={loading} className="btn-primary w-full">
              {loading ? <Loader2 className="h-4 w-4 animate-spin" /> : null}
              {loading ? "Analyzing…" : "Estimate Risk"}
            </button>
            <p className="text-xs text-slate-600">
              Based on historical landslide data from Tehri Garhwal region.
            </p>
          </form>
        </Card>

        <Card title="Risk Estimate">
          {!result && !loading && (
            <p className="text-sm text-slate-700 py-8 text-center">
              Enter the conditions above to see your risk estimate.
            </p>
          )}
          {loading && <p className="text-sm text-slate-700 py-8 text-center">Calculating…</p>}
          {result && (
            <div className="space-y-6">
              <div className="flex items-center justify-between">
                <RiskBadge level={result.riskLevel} size="lg" />
                <div className="text-right">
                  <p className="text-3xl font-bold text-slate-900">{result.confidence}%</p>
                  <p className="text-xs text-slate-600">confidence</p>
                </div>
              </div>

              <div>
                <p className="text-xs text-slate-600 uppercase tracking-wide mb-2">Why this risk level</p>
                <ul className="space-y-2">
                  {result.reasons.map((r) => (
                    <li key={r} className="flex items-start gap-2 text-sm text-slate-700">
                      <span className="h-1.5 w-1.5 rounded-full bg-forest-500 mt-1.5 shrink-0" />
                      {r}
                    </li>
                  ))}
                </ul>
              </div>

              <div>
                <p className="text-xs text-slate-600 uppercase tracking-wide mb-2">Important factors</p>
                <div className="space-y-2">
                  {result.factorWeights.map((f) => (
                    <div key={f.factor}>
                      <div className="flex justify-between text-xs text-slate-600 mb-1">
                        <span>{f.factor}</span>
                        <span>{Math.round(f.weight * 100)}%</span>
                      </div>
                      <div className="h-1.5 rounded bg-slate-700 overflow-hidden">
                        <div
                          className="h-full bg-forest-500"
                          style={{ width: `${f.weight * 100}%` }}
                        />
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}
        </Card>
      </div>
    </div>
  );
}
