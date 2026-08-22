import os
from flask import Flask, jsonify

from app.config import Config
from app.extensions import db, jwt, cors, migrate


def create_app(config_class=Config):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_class)

    os.makedirs(app.instance_path, exist_ok=True)
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

    # --- extensions ---
    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)
    cors.init_app(
        app,
        resources={r"/api/*": {"origins": app.config["FRONTEND_ORIGIN"]}},
        supports_credentials=True,
    )

    # --- models (imported so SQLAlchemy/Flask-Migrate see them) ---
    from app import models  # noqa: F401

    # --- blueprints ---
    from app.routes.auth import auth_bp
    from app.routes.districts import districts_bp
    from app.routes.predict import predict_bp
    from app.routes.weather import weather_bp
    from app.routes.incidents import incidents_bp
    from app.routes.admin import admin_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(districts_bp)
    app.register_blueprint(predict_bp)
    app.register_blueprint(weather_bp)
    app.register_blueprint(incidents_bp)
    app.register_blueprint(admin_bp)

    @app.get("/api/health")
    def health():
        return jsonify({"status": "ok", "service": "pahadsuraksha-backend"}), 200

    @app.errorhandler(404)
    def not_found(_e):
        return jsonify({"error": "Not found."}), 404

    @app.errorhandler(500)
    def server_error(_e):
        return jsonify({"error": "Internal server error."}), 500

    return app
