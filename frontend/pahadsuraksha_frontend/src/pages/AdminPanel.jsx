import { useEffect, useState } from "react";
import "../styles/adminpanel.css";
import { getStoredToken, getStoredUser, isAdminRole } from "../utils/auth";

function AdminPanel() {
  const [reports, setReports] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [approvedCount, setApprovedCount] = useState(0);
  const [rejectedCount, setRejectedCount] = useState(0);
  const [selectedMedia, setSelectedMedia] = useState(null);

  useEffect(() => {
    const loadReports = async () => {
      const storedUser = getStoredUser();
      const isAdmin = isAdminRole(storedUser?.role);

      if (!isAdmin) {
        window.location.href = "/dashboard";
        return;
      }

      const token = getStoredToken();
      if (!token) {
        window.location.href = "/login";
        return;
      }
      try {
        setLoading(true);
        setError("");

        const response = await fetch("/api/admin/pending", {
          headers: {
            Authorization: `Bearer ${token}`
          }
        });

        const data = await response.json().catch(() => ({}));

        if (!response.ok) {
          throw new Error(data.message || "Unable to fetch pending reports.");
        }

        setReports(data.reports || []);
      } catch (err) {
        setError(err.message || "Unable to load pending reports.");
      } finally {
        setLoading(false);
      }
    };

    loadReports();
  }, []);

  const approveReport = async (id) => {
    const token = getStoredToken();

    try {
      const response = await fetch(`/api/admin/approve/${id}`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
          Authorization: token ? `Bearer ${token}` : ""
        },
        body: JSON.stringify({ remark: "Verified by Disaster Management Authority." })
      });

      const data = await response.json().catch(() => ({}));

      if (!response.ok) {
        throw new Error(data.message || data.error || "Unable to approve report.");
      }

      setReports((prev) => prev.filter((report) => report.id !== id));
      setApprovedCount((prev) => prev + 1);
    } catch (err) {
      alert(err.message || "Unable to approve report.");
    }
  };

  const rejectReport = async (id) => {
    const token = getStoredToken();

    try {
      const response = await fetch(`/api/admin/reject/${id}`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
          Authorization: token ? `Bearer ${token}` : ""
        },
        body: JSON.stringify({ remark: "Report rejected after verification." })
      });

      const data = await response.json().catch(() => ({}));

      if (!response.ok) {
        throw new Error(data.message || data.error || "Unable to reject report.");
      }

      setReports((prev) => prev.filter((report) => report.id !== id));
      setRejectedCount((prev) => prev + 1);
    } catch (err) {
      alert(err.message || "Unable to reject report.");
    }
  };

  const openMediaPreview = (report) => {
    if (report.image) {
      setSelectedMedia({
        type: "image",
        src: `/api/media/images/${report.image}`
      });
      return;
    }

    if (report.video) {
      setSelectedMedia({
        type: "video",
        src: `/api/media/videos/${report.video}`
      });
      return;
    }

    setSelectedMedia(null);
  };

  return (
    <div className="admin-page">
      <div className="admin-header">
        <h1>Disaster Official Dashboard</h1>
        <p>Approve or Reject Citizen Incidents</p>
      </div>

      <div className="stats">
        <div className="stat-card">
          <h2>Pending</h2>
          <h1>{reports.length}</h1>
        </div>

        <div className="stat-card">
          <h2>Approved</h2>
          <h1>{approvedCount}</h1>
        </div>

        <div className="stat-card">
          <h2>Rejected</h2>
          <h1>{rejectedCount}</h1>
        </div>
      </div>

      {loading && <p>Loading reports...</p>}
      {error && <p>{error}</p>}

      {!loading && !error && reports.length === 0 && (
        <p>No pending reports available for verification.</p>
      )}

      {selectedMedia && (
        <div className="media-modal" onClick={() => setSelectedMedia(null)}>
          <div className="media-modal-content" onClick={(e) => e.stopPropagation()}>
            <button className="media-modal-close" onClick={() => setSelectedMedia(null)}>
              ✕
            </button>
            {selectedMedia.type === "image" ? (
              <img src={selectedMedia.src} alt="Uploaded media preview" className="media-modal-image" />
            ) : (
              <video controls className="media-modal-video" src={selectedMedia.src} />
            )}
          </div>
        </div>
      )}

      <div className="report-list">
        {reports.map((report) => (
          <div className="report-card" key={report.id}>
            <h2>{report.title}</h2>
            <p><strong>ID :</strong> {report.id}</p>
            <p><strong>Location :</strong> {report.location}</p>
            <p><strong>District :</strong> {report.district}</p>
            <p><strong>Severity :</strong> {report.severity}</p>
            <p><strong>Reported By :</strong> {report.user_id ? "Citizen" : "Unknown"}</p>
            <p><strong>Date :</strong> {report.created_at || "N/A"}</p>
            <p><strong>Status :</strong> {report.status || "Pending"}</p>
            <p><strong>AI Verification :</strong> 🟡 Pending Review</p>
            <p><strong>Description :</strong> {report.description}</p>

            <div className="media-preview-box">
              {report.image ? (
                <>
                  <img
                    src={`/api/media/images/${report.image}`}
                    alt={report.title}
                    className="media-thumbnail"
                    onClick={() => openMediaPreview(report)}
                  />
                  <p className="media-hint">Click the image to enlarge it</p>
                </>
              ) : report.video ? (
                <button className="media-link-btn" onClick={() => openMediaPreview(report)}>
                  Open uploaded video
                </button>
              ) : (
                <p className="media-empty">No media uploaded for this report.</p>
              )}
            </div>

            <div className="button-group">
              <button className="view-btn">View Map</button>
              <button className="approve-btn" onClick={() => approveReport(report.id)}>
                Approve
              </button>
              <button className="reject-btn" onClick={() => rejectReport(report.id)}>
                Reject
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default AdminPanel;