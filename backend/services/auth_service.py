from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity
)

from models.user import User
from models import db


# =====================================================
# Authentication Service
# =====================================================

class AuthService:

    def __init__(self):

        pass


    # =================================================
    # Hash Password
    # =================================================

    def hash_password(self, password):

        return generate_password_hash(

            password,

            method="pbkdf2:sha256"

        )


    # =================================================
    # Verify Password
    # =================================================

    def verify_password(

        self,

        password,

        hashed_password

    ):

        return check_password_hash(

            hashed_password,

            password

        )


    # =================================================
    # Check Email Exists
    # =================================================

    def email_exists(self, email):

        user = User.query.filter_by(

            email=email

        ).first()

        return user is not None


    # =================================================
    # Find User By Email
    # =================================================

    def get_user_by_email(self, email):

        return User.query.filter_by(

            email=email

        ).first()


    # =================================================
    # Find User By ID
    # =================================================

    def get_user_by_id(self, user_id):

        return User.query.get(

            user_id

        )


    # =================================================
    # Generate JWT Tokens
    # =================================================

    def generate_tokens(self, user):

        access_token = create_access_token(

            identity=str(user.id),

            additional_claims={

                "role": user.role,

                "name": user.name

            }

        )

        refresh_token = create_refresh_token(

            identity=str(user.id)

        )

        return {

            "access_token": access_token,

            "refresh_token": refresh_token

        }


    # =================================================
    # Current Logged-in User
    # =================================================

    def current_user(self):

        user_id = get_jwt_identity()

        if user_id is None:

            return None

        return self.get_user_by_id(

            user_id

        )
        # =================================================
    # Register User
    # =================================================

    def register(

        self,

        name,

        email,

        password,

        role

    ):

        # ---------------------------------------------
        # Check Existing Email
        # ---------------------------------------------

        if self.email_exists(email):

            return {

                "success": False,

                "message": "Email already registered."

            }

        # ---------------------------------------------
        # Validate Role
        # ---------------------------------------------

        valid_roles = [

            "Citizen",

            "Official"

        ]

        if role not in valid_roles:

            return {

                "success": False,

                "message": "Invalid user role."

            }

        # ---------------------------------------------
        # Create User
        # ---------------------------------------------

        new_user = User(

            name=name,

            email=email,

            password=self.hash_password(

                password

            ),

            role=role

        )

        db.session.add(

            new_user

        )

        db.session.commit()

        tokens = self.generate_tokens(

            new_user

        )

        return {

            "success": True,

            "message": "Registration successful.",

            "user": {

                "id": new_user.id,

                "name": new_user.name,

                "email": new_user.email,

                "role": new_user.role

            },

            "tokens": tokens

        }


    # =================================================
    # Login User
    # =================================================

    def login(

        self,

        email,

        password

    ):

        user = self.get_user_by_email(

            email

        )

        if user is None:

            return {

                "success": False,

                "message": "User not found."

            }

        if not self.verify_password(

            password,

            user.password

        ):

            return {

                "success": False,

                "message": "Invalid password."

            }

        tokens = self.generate_tokens(

            user

        )

        return {

            "success": True,

            "message": "Login successful.",

            "user": {

                "id": user.id,

                "name": user.name,

                "email": user.email,

                "role": user.role

            },

            "tokens": tokens

        }


    # =================================================
    # Refresh Access Token
    # =================================================

    def refresh_access_token(

        self,

        user

    ):

        access_token = create_access_token(

            identity=str(user.id),

            additional_claims={

                "role": user.role,

                "name": user.name

            }

        )

        return {

            "success": True,

            "access_token": access_token

        }


    # =================================================
    # Login Response
    #
    # Standard response returned to React frontend
    # =================================================

    def auth_response(

        self,

        user

    ):

        tokens = self.generate_tokens(

            user

        )

        return {

            "user": {

                "id": user.id,

                "name": user.name,

                "email": user.email,

                "role": user.role

            },

            "access_token":

                tokens["access_token"],

            "refresh_token":

                tokens["refresh_token"]

        }
        # =================================================
    # Get User Profile
    # =================================================

    def user_profile(self):

        user = self.current_user()

        if user is None:

            return {

                "success": False,

                "message": "User not found."

            }

        return {

            "success": True,

            "user": {

                "id": user.id,

                "name": user.name,

                "email": user.email,

                "role": user.role,

                "created_at": user.created_at

            }

        }


    # =================================================
    # Check User Role
    # =================================================

    def has_role(

        self,

        role

    ):

        user = self.current_user()

        if user is None:

            return False

        return user.role == role


    # =================================================
    # Check Official Access
    # =================================================

    def is_official(self):

        return self.has_role(

            "Official"

        )


    # =================================================
    # Check Citizen Access
    # =================================================

    def is_citizen(self):

        return self.has_role(

            "Citizen"

        )


    # =================================================
    # Change Password
    # =================================================

    def change_password(

        self,

        current_password,

        new_password

    ):

        user = self.current_user()

        if user is None:

            return {

                "success": False,

                "message": "User not found."

            }

        if not self.verify_password(

            current_password,

            user.password

        ):

            return {

                "success": False,

                "message": "Current password is incorrect."

            }

        user.password = self.hash_password(

            new_password

        )

        db.session.commit()

        return {

            "success": True,

            "message": "Password updated successfully."

        }


    # =================================================
    # Update User Profile
    # =================================================

    def update_profile(

        self,

        name,

        email

    ):

        user = self.current_user()

        if user is None:

            return {

                "success": False,

                "message": "User not found."

            }

        existing = User.query.filter_by(

            email=email

        ).first()

        if existing and existing.id != user.id:

            return {

                "success": False,

                "message": "Email already exists."

            }

        user.name = name

        user.email = email

        db.session.commit()

        return {

            "success": True,

            "message": "Profile updated successfully.",

            "user": {

                "id": user.id,

                "name": user.name,

                "email": user.email,

                "role": user.role

            }

        }


    # =================================================
    # Delete User Account
    # =================================================

    def delete_account(self):

        user = self.current_user()

        if user is None:

            return {

                "success": False,

                "message": "User not found."

            }

        db.session.delete(

            user

        )

        db.session.commit()

        return {

            "success": True,

            "message": "Account deleted successfully."

        }
        # =================================================
    # Logout
    #
    # JWT logout is handled on frontend by
    # deleting the stored access & refresh tokens.
    # =================================================

    def logout(self):

        return {

            "success": True,

            "message": "Logged out successfully."

        }


    # =================================================
    # Authentication Health Check
    # =================================================

    def health_check(self):

        return {

            "service": "Authentication Service",

            "status": "Running"

        }


    # =================================================
    # Reset Password
    #
    # Placeholder
    # Future:
    # Email OTP Integration
    # =================================================

    def reset_password(

        self,

        email,

        new_password

    ):

        user = self.get_user_by_email(

            email

        )

        if user is None:

            return {

                "success": False,

                "message": "User not found."

            }

        user.password = self.hash_password(

            new_password

        )

        db.session.commit()

        return {

            "success": True,

            "message": "Password reset successfully."

        }


    # =================================================
    # Validate Access Token
    # =================================================

    def validate_user(self):

        user = self.current_user()

        if user is None:

            return {

                "success": False,

                "message": "Invalid token."

            }

        return {

            "success": True,

            "user": {

                "id": user.id,

                "name": user.name,

                "email": user.email,

                "role": user.role

            }

        }


# =====================================================
# Singleton Instance
# =====================================================

auth_service = AuthService()


# =====================================================
# Utility Functions
# =====================================================

def register_user(

    name,

    email,

    password,

    role

):

    return auth_service.register(

        name,

        email,

        password,

        role

    )


def login_user(

    email,

    password

):

    return auth_service.login(

        email,

        password

    )


def current_user():

    return auth_service.current_user()


def user_profile():

    return auth_service.user_profile()


def change_password(

    current_password,

    new_password

):

    return auth_service.change_password(

        current_password,

        new_password

    )


def update_profile(

    name,

    email

):

    return auth_service.update_profile(

        name,

        email

    )


def delete_account():

    return auth_service.delete_account()


def logout():

    return auth_service.logout()


def auth_health():

    return auth_service.health_check()


def validate_user():

    return auth_service.validate_user()