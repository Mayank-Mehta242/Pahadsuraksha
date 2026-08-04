from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from models import db, init_models

# Configuration
from config import Config



# =====================================================
# Create Flask App
# =====================================================

app = Flask(__name__)

# Load Configuration
app.config.from_object(Config)

# Enable CORS
CORS(app)

# Initialize JWT
app.config["JWT_TOKEN_LOCATION"] = ["headers"]
app.config["JWT_HEADER_NAME"] = "Authorization"
app.config["JWT_HEADER_TYPE"] = "Bearer"
jwt = JWTManager(app)

# Initialize Database
db.init_app(app)
init_models()

# =====================================================
# Import Blueprints
# =====================================================

from routes.auth import auth_bp
from routes.weather import weather_bp
from routes.prediction import prediction_bp
from routes.incident import incident_bp
from routes.admin import admin_bp
from routes.dashboard import dashboard_bp

# =====================================================
# Register Blueprints
# =====================================================

app.register_blueprint(auth_bp, url_prefix="/api/auth")

app.register_blueprint(weather_bp, url_prefix="/api/weather")

app.register_blueprint(prediction_bp, url_prefix="/api/prediction")

app.register_blueprint(incident_bp, url_prefix="/api/incident")

app.register_blueprint(admin_bp, url_prefix="/api/admin")

app.register_blueprint(dashboard_bp, url_prefix="/api/dashboard")

# =====================================================
# Home Route
# =====================================================

@app.route("/")
def home():
    return {
        "message": "Welcome to PAHADSURAKSHA Backend API",
        "status": "Running"
    }

# =====================================================
# Create Database Tables
# =====================================================

with app.app_context():
    db.create_all()

# =====================================================
# Run Server
# =====================================================

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )