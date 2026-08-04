"""
=====================================================
PAHADSURAKSHA Backend Routes Package
=====================================================

This package contains all API routes used in the
PAHADSURAKSHA backend.

Modules:

1. auth.py
   - User Registration
   - User Login
   - User Profile

2. weather.py
   - Live Weather API
   - Weather Forecast
   - Weather Alerts

3. prediction.py
   - AI Landslide Prediction
   - Route Safety Prediction

4. incident.py
   - Report Incident
   - View User Reports

5. admin.py
   - Approve Incident
   - Reject Incident
   - Delete Incident

6. dashboard.py
   - Dashboard Statistics
   - Recent Incidents
   - Live Monitoring

=====================================================
"""

from .auth import auth_bp
from .weather import weather_bp
from .prediction import prediction_bp
from .incident import incident_bp
from .admin import admin_bp
from .dashboard import dashboard_bp

__all__ = [

    "auth_bp",

    "weather_bp",

    "prediction_bp",

    "incident_bp",

    "admin_bp",

    "dashboard_bp"

]