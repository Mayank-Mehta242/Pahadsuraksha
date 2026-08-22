from app.extensions import db


class District(db.Model):
    __tablename__ = "districts"

    id = db.Column(db.String(60), primary_key=True)  # slug, e.g. "chamoli"
    name = db.Column(db.String(120), nullable=False)
    lat = db.Column(db.Float, nullable=False)
    lng = db.Column(db.Float, nullable=False)
    current_risk = db.Column(db.String(20), nullable=False, default="low")  # low|medium|high|extreme
    incidents_ytd = db.Column(db.Integer, nullable=False, default=0)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "lat": self.lat,
            "lng": self.lng,
            "risk": self.current_risk,
            "incidents": self.incidents_ytd,
        }
