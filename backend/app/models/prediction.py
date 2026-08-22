import uuid
from datetime import datetime, timezone
from app.extensions import db


class Prediction(db.Model):
    __tablename__ = "predictions"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey("users.id"), nullable=True)

    rainfall = db.Column(db.Float, nullable=False)
    humidity = db.Column(db.Float, nullable=False)
    temperature = db.Column(db.Float, nullable=False)
    elevation = db.Column(db.Float, nullable=False)
    slope = db.Column(db.Float, nullable=False)
    historical_incidents = db.Column(db.Float, nullable=False)

    risk_level = db.Column(db.String(20), nullable=False)
    confidence = db.Column(db.Float, nullable=False)

    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        return {
            "id": self.id,
            "riskLevel": self.risk_level,
            "confidence": self.confidence,
            "createdAt": self.created_at.isoformat(),
        }
