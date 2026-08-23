import { useEffect, useState } from "react";
import toast from "react-hot-toast";
import { Check, X, Eye, Trash2, FileDown, FileSpreadsheet } from "lucide-react";
import Card from "../components/Card.jsx";
import LoadingSpinner from "../components/LoadingSpinner.jsx";
import { incidentService } from "../services/incidentService.js";

export default function AdminDashboardPage() {
  const [reports, setReports] = useState(null);
  const [preview, setPreview] = useState(null);
  const [comments, setComments] = useState({});

  useEffect(() => {
    incidentService.list().then(setReports);
  }, []);

  async function handleApprove(id) {
    const comment = comments[id] || "";
    const updated = await incidentService.approve(id, comment);
    setReports((r) => r.map((rep) => (rep.id === id ? { ...rep, ...updated } : rep)));
    toast.success("Report approved.");
  }

  async function handleReject(id) {
    const comment = comments[id] || "";
    const updated = await incidentService.reject(id, comment);
    setReports((r) => r.map((rep) => (rep.id === id ? { ...rep, ...updated } : rep)));
    toast.success("Report rejected.");
  }

  async function handleDelete(id) {
    await incidentService.delete(id);
    setReports((r) => r.filter((rep) => rep.id !== id));
    toast.success("Report deleted.");
  }

  return (
    <div>
      <h1 className="text-2xl font-bold text-white mb-6">District Officer Panel</h1>

      <Card
        title="Incident reports queue"
        action={
          <div className="flex gap-2">
            <button className="btn-secondary !px-3 !py-1.5 text-xs">
              <FileSpreadsheet className="h-3.5 w-3.5" /> Export CSV
            </button>
            <button className="btn-secondary !px-3 !py-1.5 text-xs">
              <FileDown className="h-3.5 w-3.5" /> Export PDF
            </button>
          </div>
        }
      >
        {!reports ? (
          <LoadingSpinner label="Loading reports" />
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="text-left text-xs text-slate-300 uppercase tracking-wide border-b border-white/5">
                  <th className="pb-3 pr-4">Title</th>
                  <th className="pb-3 pr-4">District</th>
                  <th className="pb-3 pr-4">Evidence</th>
                  <th className="pb-3 pr-4">Date</th>
                  <th className="pb-3 pr-4">Status</th>
                  <th className="pb-3">Action</th>
                </tr>
              </thead>
              <tbody>
                {reports.map((r) => (
                  <tr key={r.id} className="border-b border-white/5 last:border-0">
                    <td className="py-3 pr-4 text-white">{r.title}</td>
                    <td className="py-3 pr-4 text-slate-200">{r.district}</td>
                    <td className="py-3 pr-4">
                      {r.imageUrl ? (
                        <button
                          type="button"
                          onClick={() => setPreview({ url: r.imageUrl, title: r.title })}
                          className="inline-flex items-center gap-2 text-forest-500 hover:text-forest-400"
                          aria-label={`View image for ${r.title}`}
                        >
                          <img
                            src={r.imageUrl}
                            alt={`Evidence for ${r.title}`}
                            className="h-12 w-16 rounded object-cover border border-slate-600"
                          />
                          <Eye className="h-4 w-4" />
                        </button>
                      ) : (
                        <span className="text-xs text-slate-300">No image</span>
                      )}
                    </td>
                    <td className="py-3 pr-4 text-slate-200 font-mono text-xs">{r.createdAt}</td>
                    <td className="py-3 pr-4">
                      <StatusPill status={r.status} />
                    </td>
                    <td className="py-3">
                      {r.status === "pending" ? (
                        <div className="min-w-56 space-y-2">
                          <textarea
                            value={comments[r.id] || ""}
                            onChange={(e) => setComments((current) => ({ ...current, [r.id]: e.target.value }))}
                            placeholder="Add a review comment"
                            maxLength={2000}
                            rows={2}
                            className="input-field text-xs resize-y"
                          />
                          <div className="flex gap-2">
                          <button
                            onClick={() => handleApprove(r.id)}
                            className="p-1.5 rounded-md bg-risk-low/15 text-risk-low hover:bg-risk-low/25"
                            aria-label={`Approve ${r.title}`}
                          >
                            <Check className="h-3.5 w-3.5" />
                          </button>
                          <button
                            onClick={() => handleReject(r.id)}
                            className="p-1.5 rounded-md bg-risk-extreme/15 text-risk-extreme hover:bg-risk-extreme/25"
                            aria-label={`Reject ${r.title}`}
                          >
                            <X className="h-3.5 w-3.5" />
                          </button>
                          </div>
                        </div>
                      ) : r.status === "approved" ? (
                        <button
                          onClick={() => handleDelete(r.id)}
                          className="p-1.5 rounded-md bg-risk-extreme/15 text-risk-extreme hover:bg-risk-extreme/25"
                          aria-label={`Delete ${r.title}`}
                        >
                          <Trash2 className="h-3.5 w-3.5" />
                        </button>
                      ) : (
                        <span className="text-xs text-slate-300">—</span>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </Card>

      {preview && (
        <div
          className="fixed inset-0 z-50 flex items-center justify-center bg-black/75 p-4"
          role="dialog"
          aria-modal="true"
          aria-label="Incident evidence preview"
          onClick={() => setPreview(null)}
        >
          <div className="relative max-h-full max-w-4xl" onClick={(e) => e.stopPropagation()}>
            <img src={preview.url} alt={`Evidence for ${preview.title}`} className="max-h-[80vh] max-w-full rounded-lg" />
            <button
              type="button"
              onClick={() => setPreview(null)}
              className="absolute -right-3 -top-3 inline-flex items-center gap-1 rounded-full bg-slate-900 px-3 py-2 text-sm text-slate-100 shadow-lg hover:bg-slate-800"
              aria-label="Close image preview"
            >
              <X className="h-5 w-5" />
              <span>Close</span>
            </button>
          </div>
        </div>
      )}
    </div>
  );
}

function StatusPill({ status }) {
  const styles = {
    pending: "bg-risk-medium/15 text-risk-medium",
    approved: "bg-risk-low/15 text-risk-low",
    rejected: "bg-risk-extreme/15 text-risk-extreme",
  };
  return (
    <span className={`px-2.5 py-1 rounded-full text-xs font-medium capitalize ${styles[status]}`}>{status}</span>
  );
}
