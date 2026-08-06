import os
from dotenv import load_dotenv

# =====================================================
# Load Environment Variables
# =====================================================

load_dotenv()

# =====================================================
# Base Directory
# =====================================================

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# =====================================================
# Configuration Class
# =====================================================

class Config:

    # -------------------------------------------------
    # Flask Configuration
    # -------------------------------------------------

    SECRET_KEY = os.getenv(
        "SECRET_KEY",
        "pahadsuraksha_secret_key"
    )

    # -------------------------------------------------
    # Database Configuration
    # -------------------------------------------------

    SQLALCHEMY_DATABASE_URI = (
        "sqlite:///" +
        os.path.join(BASE_DIR, "database", "database.db")
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # -------------------------------------------------
    # JWT Configuration
    # -------------------------------------------------

    JWT_SECRET_KEY = os.getenv(
        "JWT_SECRET_KEY",
        "jwt_secret_key"
    )

    JWT_ACCESS_TOKEN_EXPIRES = 86400  # 24 Hours
    JWT_TOKEN_LOCATION = ["headers"]
    JWT_HEADER_NAME = "Authorization"
    JWT_HEADER_TYPE = "Bearer"

    # -------------------------------------------------
    # Upload Configuration
    # -------------------------------------------------

    UPLOAD_FOLDER = os.path.join(
        BASE_DIR,
        "uploads"
    )

    IMAGE_FOLDER = os.path.join(
        UPLOAD_FOLDER,
        "images"
    )

    VIDEO_FOLDER = os.path.join(
        UPLOAD_FOLDER,
        "videos"
    )

    MAX_CONTENT_LENGTH = 50 * 1024 * 1024   # 50 MB

    # -------------------------------------------------
    # OpenWeather API
    # -------------------------------------------------

    OPENWEATHER_API_KEY = os.getenv(
        "OPENWEATHER_API_KEY",
        ""
    )

    # -------------------------------------------------
    # OpenRouteService API
    # -------------------------------------------------

    OPENROUTESERVICE_API_KEY = os.getenv(
        "OPENROUTESERVICE_API_KEY",
        ""
    )

    # -------------------------------------------------
    # AI Model
    # -------------------------------------------------

    MODEL_PATH = os.path.join(
        BASE_DIR,
        "ml",
        "model.pkl"
    )

    # -------------------------------------------------
    # Allowed File Extensions
    # -------------------------------------------------

    ALLOWED_IMAGE_EXTENSIONS = {
        "png",
        "jpg",
        "jpeg"
    }

    ALLOWED_VIDEO_EXTENSIONS = {
         "mp4",
        "mov",
        "avi"
    }