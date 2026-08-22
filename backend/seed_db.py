"""
Creates all tables and seeds Tehri Garhwal plus one demo admin account.
Safe to re-run — it reconciles the monitored district and skips existing users.

Usage:
    python seed_db.py
"""
from dotenv import load_dotenv
from sqlalchemy import inspect, text

load_dotenv()

from app import create_app  # noqa: E402
from app.extensions import db  # noqa: E402
from app.models.district import District  # noqa: E402
from app.models.user import User  # noqa: E402

DISTRICTS = [("tehri-garhwal", "Tehri Garhwal", 30.3752, 78.48, "medium", 12)]


def seed():
    app = create_app()
    with app.app_context():
        db.create_all()

        if "review_comment" not in {column["name"] for column in inspect(db.engine).get_columns("incidents")}:
            db.session.execute(text("ALTER TABLE incidents ADD COLUMN review_comment TEXT"))

        District.query.filter(District.id != "tehri-garhwal").delete(synchronize_session=False)
        User.query.filter(User.role.in_(["admin", "official"])).update(
            {"role": "district_officer"}, synchronize_session=False
        )
        User.query.filter(User.role.in_(["citizen", "tourist"])).update(
            {"role": "driver"}, synchronize_session=False
        )

        for slug, name, lat, lng, risk, incidents in DISTRICTS:
            if District.query.get(slug):
                continue
            db.session.add(District(id=slug, name=name, lat=lat, lng=lng, current_risk=risk, incidents_ytd=incidents))

        admin_user = User.query.filter_by(email="admin@pahadsuraksha.gov.in").first()
        if not admin_user:
            admin = User(name="District Officer", email="admin@pahadsuraksha.gov.in", role="district_officer", district="Tehri Garhwal")
            admin.set_password("ChangeMe123!")
            db.session.add(admin)
            print("Created demo admin — admin@pahadsuraksha.gov.in / ChangeMe123! (change this password)")
        else:
            admin_user.name = "District Officer"
            admin_user.role = "district_officer"
            admin_user.district = "Tehri Garhwal"

        db.session.commit()
        print(f"Seeded {District.query.count()} districts.")


if __name__ == "__main__":
    seed()
