from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

from app.extensions import db
from app.models.user import User

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")


@auth_bp.post("/register")
def register():
    body = request.get_json(silent=True) or {}
    required = ["name", "email", "password"]
    missing = [f for f in required if not body.get(f)]
    if missing:
        return jsonify({"error": f"Missing fields: {', '.join(missing)}"}), 400

    if User.query.filter_by(email=body["email"].lower().strip()).first():
        return jsonify({"error": "An account with this email already exists."}), 409

    # Officer accounts are provisioned by seed/admin tooling, never by public signup.
    role = "driver"

    user = User(
        name=body["name"].strip(),
        email=body["email"].lower().strip(),
        district=body.get("district"),
        role=role,
        phone=body.get("phone"),
    )
    user.set_password(body["password"])
    db.session.add(user)
    db.session.commit()

    token = create_access_token(identity=user.id, additional_claims={"role": user.role})
    return jsonify({"token": token, "user": user.to_dict()}), 201


@auth_bp.post("/login")
def login():
    body = request.get_json(silent=True) or {}
    email = (body.get("email") or "").lower().strip()
    password = body.get("password") or ""

    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        return jsonify({"error": "Invalid email or password."}), 401

    token = create_access_token(identity=user.id, additional_claims={"role": user.role})
    return jsonify({"token": token, "user": user.to_dict()}), 200


@auth_bp.get("/me")
@jwt_required()
def me():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found."}), 404
    return jsonify({"user": user.to_dict()}), 200
