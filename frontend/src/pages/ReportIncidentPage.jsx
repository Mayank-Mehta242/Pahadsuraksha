import { useEffect, useState } from "react";
import toast from "react-hot-toast";
import { ImagePlus, LocateFixed, Send } from "lucide-react";
import Card from "../components/Card.jsx";
import MapView from "../components/MapView.jsx";
import { useGeolocation } from "../hooks/useGeolocation.js";
import { incidentService } from "../services/incidentService.js";
import { mockReports } from "../data/mockData.js";

export default function ReportIncidentPage() {
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [image, setImage] = useState(null);
  const [imagePreview, setImagePreview] = useState(null);
  const [coords, setCoords] = useState(null);
  const [submitting, setSubmitting] = useState(false);
  const { position, locate, locating } = useGeolocation();

  useEffect(() => {
    if (position) setCoords(position);
  }, [position]);

  function handleImage(e) {
    const file = e.target.files?.[0];
    if (!file) return;
    setImage(file);
    setImagePreview(URL.createObjectURL(file));
  }

  async function handleSubmit(e) {
    e.preventDefault();
    if (!coords) {
      toast.error("Please set a location first.");
      return;
    }
    setSubmitting(true);
    try {
      const formData = new FormData();
      formData.append("title", title);
      formData.append("description", description);
      formData.append("lat", coords.lat);
      formData.append("lng", coords.lng);
      if (image) formData.append("image", image);

      await incidentService.submit(formData);
      toast.success("Report submitted for review.");
      setTitle("");
      setDescription("");
      setImage(null);
      setImagePreview(null);
    } catch (err) {
      toast.error("Could not submit report.");
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <div className="max-w-4xl">
      <h1 className="text-3xl font-bold text-slate-900 mb-8">Report an Incident</h1>

      <div className="grid lg:grid-cols-2 gap-6">
        <Card title="Incident Details">
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="text-sm text-slate-700 mb-1.5 block">Title</label>
              <input
                required
                className="input-field"
                placeholder="e.g. Debris on NH-58 near Devprayag"
                value={title}
                onChange={(e) => setTitle(e.target.value)}
              />
            </div>

            <div>
              <label className="text-sm text-slate-700 mb-1.5 block">Description</label>
              <textarea
                required
                rows={3}
                className="input-field resize-none"
                placeholder="What did you see? How large is the affected area?"
                value={description}
                onChange={(e) => setDescription(e.target.value)}
              />
            </div>

            <div>
              <label className="text-sm text-slate-700 mb-1.5 block">Photo (optional)</label>
              <label className="flex items-center gap-3 border border-dashed border-slate-600 rounded px-4 py-3 cursor-pointer hover:border-forest-500 transition-colors">
                <ImagePlus className="h-5 w-5 text-slate-500" />
                <span className="text-sm text-slate-700">
                  {image ? image.name : "Click to upload"}
                </span>
                <input type="file" accept="image/*" className="hidden" onChange={handleImage} />
              </label>
              {imagePreview && (
                <img src={imagePreview} alt="Preview" className="mt-3 rounded max-h-40 object-cover w-full" />
              )}
            </div>

            <div className="flex items-center justify-between">
              <button type="button" onClick={locate} className="btn-secondary text-sm">
                <LocateFixed className="h-4 w-4" />
                {locating ? "Locating…" : coords ? "Set" : "My Location"}
              </button>
              {coords && (
                <span className="text-xs text-slate-600">
                  {coords.lat.toFixed(4)}, {coords.lng.toFixed(4)}
                </span>
              )}
            </div>

            <button type="submit" disabled={submitting} className="btn-primary w-full">
              {submitting ? "Submitting…" : "Submit Report"}
            </button>
          </form>
        </Card>

        <div className="space-y-4">
          <Card title="Reported Incidents" className="!p-0 overflow-hidden">
            <MapView
              districts={mockReports.map((r) => ({ ...r, name: r.title, risk: "medium" }))}
              height="280px"
            />
          </Card>
          <Card>
            <p className="text-sm text-slate-700">
              Reports are reviewed before appearing on the public map.
            </p>
          </Card>
        </div>
      </div>
    </div>
  );
}
