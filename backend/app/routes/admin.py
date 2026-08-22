import io
import csv

from flask import Blueprint, jsonify, Response, send_file
from app.models.user import User
from app.models.district import District
from app.models.incident import Incident
from app.utils.decorators import role_required

admin_bp = Blueprint("admin", __name__, url_prefix="/api/admin")


@admin_bp.get("/users")
@role_required("district_officer")
def list_users():
    users = User.query.order_by(User.created_at.desc()).all()
    return jsonify([u.to_dict() for u in users]), 200


@admin_bp.get("/analytics/districts")
@role_required("district_officer")
def district_analytics():
    districts = District.query.all()
    return (
        jsonify(
            [
                {
                    "district": d.name,
                    "risk": d.current_risk,
                    "incidents": d.incidents_ytd,
                }
                for d in districts
            ]
        ),
        200,
    )


@admin_bp.get("/export.csv")
@role_required("district_officer")
def export_csv():
    incidents = Incident.query.order_by(Incident.created_at.desc()).all()

    buffer = io.StringIO()
    writer = csv.writer(buffer)
    writer.writerow(["ID", "Title", "District", "Latitude", "Longitude", "Status", "Reported On"])
    for i in incidents:
        writer.writerow([i.id, i.title, i.district, i.lat, i.lng, i.status, i.created_at.strftime("%Y-%m-%d")])

    return Response(
        buffer.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment; filename=pahadsuraksha_incidents.csv"},
    )


@admin_bp.get("/export.pdf")
@role_required("district_officer")
def export_pdf():
    from fpdf import FPDF  # imported lazily so the app still boots without fpdf2 installed for CSV-only use

    incidents = Incident.query.order_by(Incident.created_at.desc()).all()

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 14)
    pdf.cell(0, 10, "PahadSuraksha — Incident Report Export", ln=True)
    pdf.set_font("Helvetica", "", 10)
    pdf.ln(4)

    for i in incidents:
        pdf.set_font("Helvetica", "B", 11)
        pdf.multi_cell(0, 6, f"{i.title} ({i.status})")
        pdf.set_font("Helvetica", "", 9)
        pdf.multi_cell(0, 5, f"District: {i.district or 'Unknown'}  |  Reported: {i.created_at.strftime('%Y-%m-%d')}")
        pdf.ln(3)

    output = io.BytesIO(pdf.output(dest="S"))
    output.seek(0)
    return send_file(
        output, mimetype="application/pdf", as_attachment=True, download_name="pahadsuraksha_incidents.pdf"
    )
