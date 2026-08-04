from flask_sqlalchemy import SQLAlchemy

# =====================================================
# Database Instance
# =====================================================

db = SQLAlchemy()

# =====================================================
# Import All Models
# =====================================================

def init_models():
    from .user import User
    from .incident import Incident
    from .prediction import Prediction