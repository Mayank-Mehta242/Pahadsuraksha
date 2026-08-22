from datetime import datetime, timezone
from app.extensions import db


class WeatherCache(db.Model):
    __tablename__ = "weather_cache"

    # Cache key is lat/lng rounded to ~1km precision
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    lat_key = db.Column(db.Float, nullable=False, index=True)
    lng_key = db.Column(db.Float, nullable=False, index=True)

    location_name = db.Column(db.String(120), nullable=True)
    temperature_c = db.Column(db.Float, nullable=False)
    humidity_pct = db.Column(db.Float, nullable=False)
    rainfall_mm = db.Column(db.Float, nullable=False)
    wind_kmh = db.Column(db.Float, nullable=False)
    elevation_m = db.Column(db.Float, nullable=True)
    condition = db.Column(db.String(80), nullable=True)
    forecast_json = db.Column(db.Text, nullable=True)  # JSON-encoded 7-day forecast

    fetched_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
