import os
from datetime import timedelta

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret")
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "dev-jwt-secret")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=7)

    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL", f"sqlite:///{os.path.join(BASE_DIR, 'instance', 'pahadsuraksha.db')}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    FRONTEND_ORIGIN = os.environ.get("FRONTEND_ORIGIN", "http://localhost:5173")

    OPENWEATHER_API_KEY = os.environ.get("OPENWEATHER_API_KEY", "")
    ELEVATION_API_URL = os.environ.get("ELEVATION_API_URL", "https://api.open-elevation.com/api/v1/lookup")
    WEATHER_CACHE_MINUTES = int(os.environ.get("WEATHER_CACHE_MINUTES", "30"))

    UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads", "incidents")
    MAX_CONTENT_LENGTH = 8 * 1024 * 1024  # 8 MB uploads

    ML_MODEL_PATH = os.path.join(BASE_DIR, "machine_learning", "landslide_model.pkl")
