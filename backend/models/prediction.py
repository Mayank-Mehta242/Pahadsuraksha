from datetime import datetime

from models import db


class Prediction(db.Model):

    __tablename__ = "predictions"

    # =====================================================
    # Primary Key
    # =====================================================

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    # =====================================================
    # User Relationship
    # =====================================================

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    # =====================================================
    # Route Information
    # =====================================================

    source = db.Column(
        db.String(150),
        nullable=False
    )

    destination = db.Column(
        db.String(150),
        nullable=False
    )

    # =====================================================
    # Weather Information
    # =====================================================

    weather_condition = db.Column(
        db.String(100),
        nullable=False
    )

    rainfall = db.Column(
        db.Float,
        nullable=False
    )

    humidity = db.Column(
        db.Float,
        nullable=False
    )

    temperature = db.Column(
        db.Float,
        nullable=False
    )

    wind_speed = db.Column(
        db.Float,
        nullable=False
    )

    pressure = db.Column(
        db.Float,
        nullable=True
    )

    visibility = db.Column(
        db.Float,
        nullable=True
    )

    uv_index = db.Column(
        db.Float,
        nullable=True
    )

    # =====================================================
    # AI Prediction
    # =====================================================

    risk_level = db.Column(
        db.String(30),
        nullable=False
    )

    confidence = db.Column(
        db.Float,
        nullable=False
    )

    recommendation = db.Column(
        db.Text,
        nullable=False
    )

    # =====================================================
    # Route Information
    # =====================================================

    distance = db.Column(
        db.Float,
        nullable=True
    )

    estimated_time = db.Column(
        db.String(50),
        nullable=True
    )

    # =====================================================
    # Date & Time
    # =====================================================

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    # =====================================================
    # Convert Object to Dictionary
    # =====================================================

    def to_dict(self):

        return {

            "id": self.id,

            "user_id": self.user_id,

            "source": self.source,

            "destination": self.destination,

            "weather_condition": self.weather_condition,

            "rainfall": self.rainfall,

            "humidity": self.humidity,

            "temperature": self.temperature,

            "wind_speed": self.wind_speed,

            "pressure": self.pressure,

            "visibility": self.visibility,

            "uv_index": self.uv_index,

            "risk_level": self.risk_level,

            "confidence": self.confidence,

            "recommendation": self.recommendation,

            "distance": self.distance,

            "estimated_time": self.estimated_time,

            "created_at": self.created_at.strftime(
                "%d-%m-%Y %H:%M"
            )

        }

    # =====================================================
    # String Representation
    # =====================================================

    def __repr__(self):

        return (
            f"<Prediction {self.source} -> "
            f"{self.destination}>"
        )