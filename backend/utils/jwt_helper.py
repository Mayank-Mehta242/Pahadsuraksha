from datetime import datetime, timezone

from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    decode_token,
    get_jwt_identity,
    get_jwt
)

from models.user import User


# =====================================================
# JWT Helper
# =====================================================

class JWTHelper:

    def __init__(self):

        pass


    # =================================================
    # Create Access Token
    # =================================================

    def generate_access_token(

        self,

        user

    ):

        return create_access_token(

            identity=str(user.id),

            additional_claims={

                "name": user.name,

                "email": user.email,

                "role": user.role

            }

        )


    # =================================================
    # Create Refresh Token
    # =================================================

    def generate_refresh_token(

        self,

        user

    ):

        return create_refresh_token(

            identity=str(user.id)

        )


    # =================================================
    # Generate Token Pair
    # =================================================

    def generate_tokens(

        self,

        user

    ):

        return {

            "access_token":

                self.generate_access_token(

                    user

                ),

            "refresh_token":

                self.generate_refresh_token(

                    user

                )

        }


    # =================================================
    # Decode JWT Token
    # =================================================

    def decode(

        self,

        token

    ):

        try:

            return decode_token(

                token

            )

        except Exception:

            return None


    # =================================================
    # Get User From JWT Payload
    # =================================================

    def get_user(

        self,

        token

    ):

        payload = self.decode(

            token

        )

        if payload is None:

            return None

        user_id = payload.get(

            "sub"

        )

        if user_id is None:

            return None

        return User.query.get(

            int(user_id)

        )


    # =================================================
    # Check Token Validity
    # =================================================

    def is_valid_token(

        self,

        token

    ):

        payload = self.decode(

            token

        )

        return payload is not None


    # =================================================
    # Get Current UTC Time
    # =================================================

    def current_time(self):

        return datetime.now(

            timezone.utc

        )
    # =================================================
    # Get Current Authenticated User
    # =================================================

    def current_user(self):

        try:

            user_id = get_jwt_identity()

            if user_id is None:

                return None

            return User.query.get(

                int(user_id)

            )

        except Exception:

            return None


    # =================================================
    # Get Current User Role
    # =================================================

    def current_role(self):

        claims = get_jwt()

        return claims.get(

            "role",

            None

        )


    # =================================================
    # Check Role
    # =================================================

    def has_role(

        self,

        role

    ):

        return self.current_role() == role


    # =================================================
    # Check Admin
    # =================================================

    def is_admin(self):

        return self.has_role(

            "Admin"

        )


    # =================================================
    # Check Official
    # =================================================

    def is_official(self):

        return self.has_role(

            "Official"

        )


    # =================================================
    # Check Citizen
    # =================================================

    def is_citizen(self):

        return self.has_role(

            "Citizen"

        )


    # =================================================
    # Check Multiple Roles
    # =================================================

    def has_any_role(

        self,

        roles

    ):

        role = self.current_role()

        return role in roles


    # =================================================
    # Permission Check
    # =================================================

    def has_permission(

        self,

        allowed_roles

    ):

        if not isinstance(

            allowed_roles,

            list

        ):

            allowed_roles = [

                allowed_roles

            ]

        return self.has_any_role(

            allowed_roles

        )


    # =================================================
    # Get JWT Claims
    # =================================================

    def get_claims(self):

        try:

            return get_jwt()

        except Exception:

            return {}


    # =================================================
    # Get User Information
    # =================================================

    def current_user_info(self):

        user = self.current_user()

        if user is None:

            return None

        return {

            "id": user.id,

            "name": user.name,

            "email": user.email,

            "role": user.role

        }
        # =================================================
    # Get Token Expiration
    # =================================================

    def token_expiration(

        self,

        token

    ):

        payload = self.decode(

            token

        )

        if payload is None:

            return None

        return payload.get(

            "exp"

        )


    # =================================================
    # Check Token Expired
    # =================================================

    def is_token_expired(

        self,

        token

    ):

        expiration = self.token_expiration(

            token

        )

        if expiration is None:

            return True

        current = int(

            self.current_time().timestamp()

        )

        return current >= expiration


    # =================================================
    # Remaining Token Lifetime
    # =================================================

    def remaining_time(

        self,

        token

    ):

        expiration = self.token_expiration(

            token

        )

        if expiration is None:

            return 0

        current = int(

            self.current_time().timestamp()

        )

        remaining = expiration - current

        return max(

            remaining,

            0

        )


    # =================================================
    # Refresh Token Validation
    # =================================================

    def can_refresh(

        self,

        token

    ):

        payload = self.decode(

            token

        )

        if payload is None:

            return False

        return payload.get(

            "type"

        ) == "refresh"


    # =================================================
    # Extract JWT Information
    # =================================================

    def token_information(

        self,

        token

    ):

        payload = self.decode(

            token

        )

        if payload is None:

            return None

        return {

            "identity":

                payload.get(

                    "sub"

                ),

            "token_type":

                payload.get(

                    "type"

                ),

            "issued_at":

                payload.get(

                    "iat"

                ),

            "expires_at":

                payload.get(

                    "exp"

                ),

            "jwt_id":

                payload.get(

                    "jti"

                )

        }


    # =================================================
    # Get User ID From Token
    # =================================================

    def get_user_id(

        self,

        token

    ):

        payload = self.decode(

            token

        )

        if payload is None:

            return None

        return payload.get(

            "sub"

        )


    # =================================================
    # Complete Token Validation
    # =================================================

    def validate(

        self,

        token

    ):

        if not self.is_valid_token(

            token

        ):

            return {

                "success": False,

                "message": "Invalid token."

            }

        if self.is_token_expired(

            token

        ):

            return {

                "success": False,

                "message": "Token has expired."

            }

        return {

            "success": True,

            "message": "Token is valid."

        }


    # =================================================
    # Authentication Status
    # =================================================

    def authentication_status(

        self,

        token

    ):

        validation = self.validate(

            token

        )

        if not validation["success"]:

            return validation

        user = self.get_user(

            token

        )

        if user is None:

            return {

                "success": False,

                "message": "User not found."

            }

        return {

            "success": True,

            "authenticated": True,

            "user": {

                "id": user.id,

                "name": user.name,

                "email": user.email,

                "role": user.role

            }

        }
    # =====================================================
# JWT Health Check
# =====================================================

    def health_check(self):

        return {

            "service": "JWT Helper",

            "status": "Running",

            "algorithm": "HS256"

        }


    # =================================================
    # Logout Placeholder
    #
    # Future Token Blacklist Support
    # =================================================

    def logout(

        self,

        token

    ):

        """
        Future Enhancement:
        Store token JTI inside a blacklist
        (Redis/Database)
        """

        payload = self.decode(

            token

        )

        if payload is None:

            return {

                "success": False,

                "message": "Invalid token."

            }

        return {

            "success": True,

            "message": "Logout successful."

        }


    # =================================================
    # Get JWT ID
    # =================================================

    def token_id(

        self,

        token

    ):

        payload = self.decode(

            token

        )

        if payload is None:

            return None

        return payload.get(

            "jti"

        )


    # =================================================
    # Token Summary
    # =================================================

    def token_summary(

        self,

        token

    ):

        info = self.token_information(

            token

        )

        if info is None:

            return None

        return {

            "user_id":

                info["identity"],

            "type":

                info["token_type"],

            "expires":

                info["expires_at"],

            "remaining_seconds":

                self.remaining_time(

                    token

                )

        }


# =====================================================
# Singleton Instance
# =====================================================

jwt_helper = JWTHelper()


# =====================================================
# Utility Functions
# =====================================================

def generate_access_token(user):

    return jwt_helper.generate_access_token(

        user

    )


def generate_refresh_token(user):

    return jwt_helper.generate_refresh_token(

        user

    )


def generate_tokens(user):

    return jwt_helper.generate_tokens(

        user

    )


def validate_token(token):

    return jwt_helper.validate(

        token

    )


def get_current_user():

    return jwt_helper.current_user()


def current_user_info():

    return jwt_helper.current_user_info()


def has_permission(roles):

    return jwt_helper.has_permission(

        roles

    )


def model_health():

    return jwt_helper.health_check()


def logout(token):

    return jwt_helper.logout(

        token

    )


def token_summary(token):

    return jwt_helper.token_summary(

        token

    )


# =====================================================
# Test JWT Helper
# =====================================================

if __name__ == "__main__":

    print("=" * 50)

    print("PAHADSURAKSHA JWT Helper")

    print("=" * 50)

    print()

    print(

        jwt_helper.health_check()

    )
