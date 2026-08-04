from datetime import datetime

from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash

from models import db


class User(db.Model):

    __tablename__ = "users"

    # =====================================================
    # Primary Key
    # =====================================================

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    # =====================================================
    # User Information
    # =====================================================

    name = db.Column(
        db.String(100),
        nullable=False
    )

    email = db.Column(
        db.String(120),
        unique=True,
        nullable=False
    )

    password = db.Column(
        db.String(255),
        nullable=False
    )

    district = db.Column(
        db.String(100),
        nullable=False
    )

    role = db.Column(
        db.String(30),
        nullable=False,
        default="Citizen"
    )

    # =====================================================
    # Account Information
    # =====================================================

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    # =====================================================
    # Relationship
    # One User -> Many Incident Reports
    # =====================================================

    incidents = db.relationship(
        "Incident",
        backref="user",
        lazy=True,
        cascade="all, delete"
    )

    # =====================================================
    # Password Methods
    # =====================================================

    def set_password(self, password):

        self.password = generate_password_hash(password)

    def check_password(self, password):

        return check_password_hash(
            self.password,
            password
        )

    # =====================================================
    # Convert Object to Dictionary
    # =====================================================

    def to_dict(self):

        return {

            "id": self.id,

            "name": self.name,

            "email": self.email,

            "district": self.district,

            "role": self.role,

            "created_at": self.created_at.strftime(
                "%d-%m-%Y %H:%M"
            )

        }

    # =====================================================
    # String Representation
    # =====================================================

    def __repr__(self):

        return f"<User {self.name}>"