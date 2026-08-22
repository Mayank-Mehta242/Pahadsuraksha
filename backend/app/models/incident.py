import uuid
from datetime import datetime, timezone
from app.extensions import db


class Incident(db.Model):
    __tablename__ = "incidents"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    district = db.Column(db.String(120), nullable=True)
    lat = db.Column(db.Float, nullable=False)
    lng = db.Column(db.Float, nullable=False)
    image_path = db.Column(db.String(255), nullable=True)  # relative path under uploads/
    status = db.Column(db.String(20), nullable=False, default="pending")  # pending|approved|rejected
    review_comment = db.Column(db.Text, nullable=True)
    reporter_id = db.Column(db.String(36), db.ForeignKey("users.id"), nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "district": self.district,
            "lat": self.lat,
            "lng": self.lng,
            "imageUrl": f"/api/incidents/uploads/{self.image_path}" if self.image_path else None,
            "status": self.status,
            "reviewComment": self.review_comment,
            "createdAt": self.created_at.strftime("%Y-%m-%d"),
        }
