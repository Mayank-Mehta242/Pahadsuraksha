import { useState } from "react";
import "../styles/report.css";

function Report() {

  const [report, setReport] = useState({
    title: "",
    location: "",
    severity: "",
    category: "",
    description: "",
    media: null,
    status: "Pending"
  });

  const handleChange = (e) => {
    setReport({
      ...report,
      [e.target.name]: e.target.value,
    });
  };

  const handleFileChange = (e) => {
    setReport({
      ...report,
      media: e.target.files[0],
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    const formData = new FormData();
    formData.append("title", report.title);
    formData.append("description", report.description);
    formData.append("location", report.location);
    formData.append("district", "Tehri Garhwal");
    formData.append("severity", report.severity);
    formData.append("category", report.category);
    if (report.media) {
      formData.append("image", report.media);
    }

    try {
      const response = await fetch("/api/incident/report", {
        method: "POST",
        body: formData
      });

      const data = await response.json().catch(() => ({}));

      if (!response.ok) {
        throw new Error(data.message || "Unable to submit incident report.");
      }

      alert(data.message || "Report submitted successfully. Waiting for Admin Approval.");

      setReport({
        title: "",
        location: "",
        severity: "",
        category: "",
        description: "",
        media: null,
        status: "Pending"
      });

      document.getElementById("media").value = "";
    } catch (err) {
      alert(err.message || "Unable to submit report.");
    }
  };

  return (
    <div className="report-page">

      <div className="report-card">

        <h1> Report an Incident</h1>

        <p>
          Report landslides, road blockages, floods or any hazardous
          situation to help keep travellers safe.
        </p>

        <form onSubmit={handleSubmit}>

          {/* Incident Title */}

          <div className="input-box">

            <label>Incident Title *</label>

            <input
              type="text"
              name="title"
              placeholder="Example: Landslide near Chamba"
              value={report.title}
              onChange={handleChange}
              required
            />

          </div>

          {/* Location */}

          <div className="input-box">

            <label>Location *</label>

            <input
              type="text"
              name="location"
              placeholder="Enter Location"
              value={report.location}
              onChange={handleChange}
              required
            />

          </div>

          {/* Category */}

          <div className="input-box">

            <label>Incident Category *</label>

            <select
              name="category"
              value={report.category}
              onChange={handleChange}
              required
            >
              <option value="">Select Category</option>

              <option value="Landslide">
                Landslide
              </option>

              <option value="Road Block">
                Road Block
              </option>

              <option value="Flood">
                Flood
              </option>

              <option value="Rockfall">
                Rockfall
              </option>

              <option value="Tree Fall">
                Tree Fall
              </option>

              <option value="Bridge Damage">
                Bridge Damage
              </option>

              <option value="Other">
                Other
              </option>

            </select>

          </div>

          {/* Severity */}

          <div className="input-box">

            <label>Severity *</label>

            <select
              name="severity"
              value={report.severity}
              onChange={handleChange}
              required
            >

              <option value="">Select Severity</option>

              <option value="Low">
                 Low
              </option>

              <option value="Medium">
                 Medium
              </option>

              <option value="High">
                 High
              </option>

              <option value="Very High">
                 Very High
              </option>

            </select>

          </div>

          {/* Description */}

          <div className="input-box">

            <label>Description *</label>

            <textarea
              rows="6"
              name="description"
              placeholder="Describe the incident..."
              value={report.description}
              onChange={handleChange}
              required
            />

          </div>

          {/* Upload */}

          <div className="input-box">

            <label>Upload Photo / Video</label>

            <input
              id="media"
              type="file"
              accept="image/*,video/*"
              onChange={handleFileChange}
            />

          </div>

          {/* Report Status */}

          <div className="input-box">

            <label>Report Status</label>

            <input
              type="text"
              value={report.status}
              disabled
            />

          </div>

          <button
            type="submit"
            className="submit-btn"
          >
            Submit Report
          </button>

        </form>

      </div>

    </div>
  );
}

export default Report;