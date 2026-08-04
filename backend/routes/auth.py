from flask import Blueprint
from flask import request
from flask import jsonify

from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity
)

from models import db
from models.user import User


# =====================================================
# Blueprint
# =====================================================

auth_bp = Blueprint(
    "auth",
    __name__
)


# =====================================================
# Register
# POST /api/auth/register
# =====================================================

@auth_bp.route("/register", methods=["POST"])
def register():

    data = request.get_json()

    if not data:
        return jsonify({
            "message": "No data received."
        }), 400

    name = data.get("name")
    email = data.get("email")
    password = data.get("password")
    district = data.get("district")
    role = data.get("role")

    if not all([
        name,
        email,
        password,
        district,
        role
    ]):

        return jsonify({
            "message": "All fields are required."
        }), 400

    existing_user = User.query.filter_by(
        email=email
    ).first()

    if existing_user:

        return jsonify({
            "message": "Email already exists."
        }), 409

    new_user = User(

        name=name,

        email=email,

        district=district,

        role=role

    )

    new_user.set_password(password)

    db.session.add(new_user)

    db.session.commit()

    return jsonify({

        "message": "Registration Successful"

    }), 201


# =====================================================
# Login
# POST /api/auth/login
# =====================================================

@auth_bp.route("/login", methods=["POST"])
def login():

    data = request.get_json()

    if not data:

        return jsonify({
            "message": "No data received."
        }), 400

    email = data.get("email")
    password = data.get("password")

    user = User.query.filter_by(
        email=email
    ).first()

    if user is None:

        return jsonify({

            "message": "User not found."

        }), 404

    if not user.check_password(password):

        return jsonify({

            "message": "Incorrect password."

        }), 401

    access_token = create_access_token(

        identity=str(user.id)

    )

    return jsonify({

        "message": "Login Successful",

        "token": access_token,

        "user": {

            "id": user.id,

            "name": user.name,

            "email": user.email,

            "district": user.district,

            "role": user.role

        }

    }), 200


# =====================================================
# Get Logged In User
# GET /api/auth/profile
# =====================================================

@auth_bp.route("/profile", methods=["GET"])
@jwt_required()
def profile():

    user_id = get_jwt_identity()

    user = User.query.get(user_id)

    if user is None:

        return jsonify({

            "message": "User not found."

        }), 404

    return jsonify(

        user.to_dict()

    ), 200


# =====================================================
# Update Profile
# PUT /api/auth/profile
# =====================================================

@auth_bp.route("/profile", methods=["PUT"])
@jwt_required()
def update_profile():

    user_id = get_jwt_identity()

    user = User.query.get(user_id)

    if user is None:

        return jsonify({

            "message": "User not found."

        }), 404

    data = request.get_json()

    user.name = data.get(

        "name",

        user.name

    )

    user.district = data.get(

        "district",

        user.district

    )

    db.session.commit()

    return jsonify({

        "message": "Profile Updated",

        "user": user.to_dict()

    }), 200


# =====================================================
# Change Password
# PUT /api/auth/change-password
# =====================================================

@auth_bp.route("/change-password", methods=["PUT"])
@jwt_required()
def change_password():

    user_id = get_jwt_identity()

    user = User.query.get(user_id)

    data = request.get_json()

    current_password = data.get(

        "currentPassword"

    )

    new_password = data.get(

        "newPassword"

    )

    if not user.check_password(current_password):

        return jsonify({

            "message": "Current password is incorrect."

        }), 400

    user.set_password(new_password)

    db.session.commit()

    return jsonify({

        "message": "Password Changed Successfully"

    }), 200


# =====================================================
# Verify Token
# GET /api/auth/verify
# =====================================================

@auth_bp.route("/verify", methods=["GET"])
@jwt_required()
def verify():

    return jsonify({

        "message": "Token Valid"

    }), 200