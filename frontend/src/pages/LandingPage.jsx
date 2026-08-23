import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { ArrowRight, CalendarDays, MapPin, MessageSquare } from "lucide-react";
import Card from "../components/Card.jsx";
import LoadingSpinner from "../components/LoadingSpinner.jsx";
import { incidentService } from "../services/incidentService.js";

export default function LandingPage() {
  const [incidents, setIncidents] = useState(null);

  useEffect(() => {
    incidentService.list("approved").then(setIncidents);
  }, []);

  return (
    <div>
      {/* Hero */}
      <section className="bg-[#536b4d] border-b border-[#718569] py-20 px-4">
        <div className="max-w-3xl mx-auto text-center">
          <h1 className="text-4xl font-bold text-white mb-6">
            Check if mountain roads are safe to travel
          </h1>
          <p className="text-lg text-slate-200 mb-8">
            Before you drive through Tehri Garhwal, check the current weather and landslide risk for your route. 
            Enter the conditions and get an estimated risk level in seconds.
          </p>
          <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
            <Link to="/dashboard/risk" className="btn-primary">
              Check Travel Risk <ArrowRight className="h-4 w-4" />
            </Link>
            <Link to="/report-incident" className="btn-secondary">
              Report an Incident
            </Link>
          </div>
        </div>
      </section>

      {/* Approved Incidents */}
      <section className="max-w-3xl mx-auto px-4 py-12">
        <h2 className="text-2xl font-bold text-slate-900 mb-8">Approved incident reports</h2>
        {!incidents ? (
          <LoadingSpinner label="Loading approved incidents" />
        ) : incidents.length === 0 ? (
          <div className="card bg-[#303a2e] text-center text-white">No approved incident reports yet.</div>
        ) : (
          <div className="grid gap-4 sm:grid-cols-2">
            {incidents.map((incident) => (
              <Card key={incident.id} className="p-5 bg-[#303a2e]">
                {incident.imageUrl && (
                  <img
                    src={incident.imageUrl}
                    alt={`Evidence for ${incident.title}`}
                    className="mb-4 h-40 w-full rounded object-cover border border-slate-600"
                  />
                )}
                <h3 className="font-semibold text-white">{incident.title}</h3>
                <div className="mt-3 flex flex-wrap gap-3 text-xs text-slate-200">
                  <span className="inline-flex items-center gap-1"><MapPin className="h-3.5 w-3.5" />{incident.district}</span>
                  <span className="inline-flex items-center gap-1"><CalendarDays className="h-3.5 w-3.5" />{incident.createdAt}</span>
                </div>
                {incident.reviewComment && (
                  <p className="mt-3 inline-flex gap-2 text-sm text-slate-200">
                    <MessageSquare className="h-4 w-4 shrink-0 text-forest-500" />
                    {incident.reviewComment}
                  </p>
                )}
              </Card>
            ))}
          </div>
        )}
      </section>

    </div>
  );
}
