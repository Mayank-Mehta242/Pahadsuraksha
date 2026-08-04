from datetime import datetime

from models import db


class Incident(db.Model):

    __tablename__ = "incidents"

    # =====================================================
    # Primary Key
    # =====================================================

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    # =====================================================
    # Incident Information
    # =====================================================

    title = db.Column(
        db.String(150),
        nullable=False
    )

    description = db.Column(
        db.Text,
        nullable=False
    )

    location = db.Column(
        db.String(200),
        nullable=False
    )

    district = db.Column(
        db.String(100),
        nullable=False
    )

    severity = db.Column(
        db.String(30),
        nullable=False
    )

    # =====================================================
    # Media Uploads
    # =====================================================

    image = db.Column(
        db.String(255),
        nullable=True
    )

    video = db.Column(
        db.String(255),
        nullable=True
    )

    # =====================================================
    # Admin Verification
    # =====================================================

    status = db.Column(
        db.String(30),
        nullable=False,
        default="Pending"
    )

    admin_remark = db.Column(
        db.Text,
        nullable=True
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
    # Date & Time
    # =====================================================

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    # =====================================================
    # Convert Object to Dictionary
    # =====================================================

    def to_dict(self):

        return {

            "id": self.id,

            "title": self.title,

            "description": self.description,

            "location": self.location,

            "district": self.district,

            "severity": self.severity,

            "image": self.image,

            "video": self.video,

            "status": self.status,

            "admin_remark": self.admin_remark,

            "user_id": self.user_id,

            "created_at": self.created_at.strftime(
                "%d-%m-%Y %H:%M"
            ),

            "updated_at": self.updated_at.strftime(
                "%d-%m-%Y %H:%M"
            )

        }

    # =====================================================
    # String Representation
    # =====================================================

    def __repr__(self):

        return f"<Incident {self.title}>"