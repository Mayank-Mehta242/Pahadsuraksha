import { useEffect, useState } from "react";
import "../styles/adminpanel.css";

function AdminPanel() {
  useEffect(() => {
    const storedUser = JSON.parse(localStorage.getItem("user") || "null");
    const role = (storedUser?.role || "").toLowerCase();
    const isAdmin = role.includes("official") || role.includes("admin") || role.includes("disaster");

    if (!isAdmin) {
      window.location.href = "/dashboard";
    }
  }, []);

  /* ===============================================
      Reports fetched from backend

      GET /api/admin/reports

      Should return only Pending reports
  =============================================== */

  const [reports, setReports] = useState([
    {
      id: 1001,
      title: "Landslide near Chamba",
      location: "Chamba",
      severity: "Very High",
      category: "Landslide",
      reporter: "Citizen",
      date: "01 Aug 2026",
      time: "10:45 AM",
      description: "Large rocks blocking NH road.",
      image: "No Image",
      aiScore: "91%"
    },
    {
      id: 1002,
      title: "Tree Fall",
      location: "New Tehri",
      severity: "Medium",
      category: "Tree Fall",
      reporter: "Citizen",
      date: "01 Aug 2026",
      time: "09:30 AM",
      description: "Tree fallen on roadside.",
      image: "No Image",
      aiScore: "82%"
    }
  ]);

  const [approvedCount, setApprovedCount] = useState(0);
  const [rejectedCount, setRejectedCount] = useState(0);



  /* ===============================================

      Approve Report

      PUT

      /api/admin/approve/:id

  =============================================== */

  const approveReport = (id) => {
    setReports((prev) => prev.filter((report) => report.id !== id));
    setApprovedCount((prev) => prev + 1);
  };



  /* ===============================================

      Reject Report

      PUT

      /api/admin/reject/:id

  =============================================== */

  const rejectReport = (id) => {
    setReports((prev) => prev.filter((report) => report.id !== id));
    setRejectedCount((prev) => prev + 1);
  };



  return (

<div className="admin-page">

<div className="admin-header">

<h1>

Disaster Official Dashboard

</h1>

<p>

Approve or Reject Citizen Reports

</p>

</div>





<div className="stats">

<div className="stat-card">

<h2>

Pending

</h2>

<h1>

{reports.length}

</h1>

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





<div className="report-list">

{

reports.map((report)=>(

<div

className="report-card"

key={report.id}

>

<h2>

{report.title}

</h2>

<p>

<strong>ID :</strong>

{report.id}

</p>

<p>

<strong>Location :</strong>

{report.location}

</p>

<p>

<strong>Severity :</strong>

{report.severity}

</p>

<p>

<strong>Category :</strong>

{report.category}

</p>

<p>

<strong>Reported By :</strong>

{report.reporter}

</p>

<p>

<strong>Date :</strong>

{report.date}

</p>

<p>

<strong>Time :</strong>

{report.time}

</p>

<p>

<strong>AI Verification :</strong>

🟢 {report.aiScore}

</p>

<p>

<strong>Description :</strong>

{report.description}

</p>

<div className="image-box">

Media Preview

</div>

<div className="button-group">

<button

className="view-btn"

>

View Map

</button>

<button

className="approve-btn"

onClick={()=>approveReport(report.id)}

>

Approve

</button>

<button

className="reject-btn"

onClick={()=>rejectReport(report.id)}

>

Reject

</button>

</div>

</div>

))

}

</div>

</div>

  );

}

export default AdminPanel;