import unittest

from flask import Flask
from flask_jwt_extended import JWTManager

from services.auth_service import AuthService


class DummyUser:
    id = 42
    role = "Citizen"
    name = "Test User"
    email = "test@example.com"


class AuthTokenTests(unittest.TestCase):
    def test_generate_tokens_accepts_integer_user_id(self):
        app = Flask(__name__)
        app.config["JWT_SECRET_KEY"] = "test-secret"
        app.config["JWT_ACCESS_TOKEN_EXPIRES"] = 3600
        app.config["JWT_TOKEN_LOCATION"] = ["headers"]
        app.config["JWT_HEADER_NAME"] = "Authorization"
        app.config["JWT_HEADER_TYPE"] = "Bearer"
        JWTManager(app)

        with app.app_context():
            tokens = AuthService().generate_tokens(DummyUser())

        self.assertIsInstance(tokens["access_token"], str)
        self.assertIsInstance(tokens["refresh_token"], str)
        self.assertTrue(tokens["access_token"])
        self.assertTrue(tokens["refresh_token"])


if __name__ == "__main__":
    unittest.main()
