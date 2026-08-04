import re

from utils.helpers import (
    validate_email,
    validate_password,
    validate_phone,
    validate_name,
    clean_string,
    is_empty,
    validate_coordinates,
    validate_city,
    to_float,
    validate_file_extension
)


# =====================================================
# Validator Class
# =====================================================

class Validator:

    # =================================================
    # Registration Validation
    # =================================================

    def validate_registration(self, data):

        errors = {}

        name = clean_string(

            data.get(

                "name",

                ""

            )

        )

        email = clean_string(

            data.get(

                "email",

                ""

            )

        ).lower()

        phone = clean_string(

            data.get(

                "phone",

                ""

            )

        )

        password = data.get(

            "password",

            ""

        )

        confirm_password = data.get(

            "confirm_password",

            ""

        )

        role = clean_string(

            data.get(

                "role",

                "Citizen"

            )

        )

        # -----------------------------
        # Name
        # -----------------------------

        if is_empty(name):

            errors["name"] = "Name is required."

        elif not validate_name(name):

            errors["name"] = "Invalid name."

        # -----------------------------
        # Email
        # -----------------------------

        if is_empty(email):

            errors["email"] = "Email is required."

        elif not validate_email(email):

            errors["email"] = "Invalid email."

        # -----------------------------
        # Phone
        # -----------------------------

        if is_empty(phone):

            errors["phone"] = "Phone number is required."

        elif not validate_phone(phone):

            errors["phone"] = "Invalid phone number."

        # -----------------------------
        # Password
        # -----------------------------

        if is_empty(password):

            errors["password"] = "Password is required."

        elif not validate_password(password):

            errors["password"] = (

                "Password must contain "

                "uppercase, lowercase, "

                "number and special character."

            )

        # -----------------------------
        # Confirm Password
        # -----------------------------

        if password != confirm_password:

            errors["confirm_password"] = (

                "Passwords do not match."

            )

        # -----------------------------
        # Role
        # -----------------------------

        allowed_roles = [

            "Citizen",

            "Official",

            "Admin"

        ]

        if role not in allowed_roles:

            errors["role"] = "Invalid role."

        return {

            "valid": len(errors) == 0,

            "errors": errors

        }


    # =================================================
    # Login Validation
    # =================================================

    def validate_login(self, data):

        errors = {}

        email = clean_string(

            data.get(

                "email",

                ""

            )

        ).lower()

        password = data.get(

            "password",

            ""

        )

        if is_empty(email):

            errors["email"] = "Email is required."

        elif not validate_email(email):

            errors["email"] = "Invalid email."

        if is_empty(password):

            errors["password"] = (

                "Password is required."

            )

        return {

            "valid": len(errors) == 0,

            "errors": errors

        }
# =====================================================
# Incident Report Validation
# =====================================================

    def validate_incident(self, data):

        errors = {}

        title = data.get("title", "").strip()
        description = data.get("description", "").strip()
        latitude = data.get("latitude")
        longitude = data.get("longitude")
        incident_type = data.get("incident_type", "").strip()

        if is_empty(title):
            errors["title"] = "Title is required."

        elif len(title) < 5:
            errors["title"] = "Title must be at least 5 characters."

        if is_empty(description):
            errors["description"] = "Description is required."

        elif len(description) < 15:
            errors["description"] = (
                "Description should contain at least 15 characters."
            )

        allowed_types = [

            "Landslide",
            "Road Block",
            "Flood",
            "Rockfall",
            "Other"

        ]

        if incident_type not in allowed_types:

            errors["incident_type"] = "Invalid incident type."

        if not validate_coordinates(

            latitude,

            longitude

        ):

            errors["coordinates"] = (

                "Invalid latitude or longitude."

            )

        return {

            "valid": len(errors) == 0,

            "errors": errors

        }


# =====================================================
# Weather Request Validation
# =====================================================

    def validate_weather_request(self, data):

        errors = {}

        city = data.get("city", "").strip()

        if is_empty(city):

            errors["city"] = "City is required."

        elif not validate_city(city):

            errors["city"] = "Invalid city."

        return {

            "valid": len(errors) == 0,

            "errors": errors

        }


# =====================================================
# Prediction Validation
# =====================================================

    def validate_prediction(self, data):

        errors = {}

        required_fields = [

            "rainfall",
            "humidity",
            "temperature",
            "wind_speed",
            "pressure",
            "visibility"

        ]

        for field in required_fields:

            if field not in data:

                errors[field] = f"{field} is required."

        if errors:

            return {

                "valid": False,

                "errors": errors

            }

        try:

            rainfall = to_float(data["rainfall"])
            humidity = to_float(data["humidity"])
            temperature = to_float(data["temperature"])
            wind_speed = to_float(data["wind_speed"])
            pressure = to_float(data["pressure"])
            visibility = to_float(data["visibility"])

            if rainfall < 0:
                errors["rainfall"] = "Rainfall cannot be negative."

            if humidity < 0 or humidity > 100:
                errors["humidity"] = (
                    "Humidity must be between 0 and 100."
                )

            if pressure <= 0:
                errors["pressure"] = "Invalid pressure."

            if visibility < 0:
                errors["visibility"] = (
                    "Visibility cannot be negative."
                )

        except Exception:

            errors["data"] = "Invalid numeric values."

        return {

            "valid": len(errors) == 0,

            "errors": errors

        }


# =====================================================
# Route Prediction Validation
# =====================================================

    def validate_route(self, data):

        errors = {}

        source = data.get(

            "source",

            ""

        ).strip()

        destination = data.get(

            "destination",

            ""

        ).strip()

        if is_empty(source):

            errors["source"] = "Source is required."

        elif not validate_city(source):

            errors["source"] = "Invalid source."

        if is_empty(destination):

            errors["destination"] = "Destination is required."

        elif not validate_city(destination):

            errors["destination"] = "Invalid destination."

        if (

            source.lower() == destination.lower()

            and

            source != ""

        ):

            errors["route"] = (

                "Source and destination cannot be the same."

            )

        return {

            "valid": len(errors) == 0,

            "errors": errors

        }
# =====================================================
# File Upload Validation
# =====================================================

    def validate_file_upload(self, file):

        errors = {}

        if file is None:

            errors["file"] = "No file uploaded."

            return {

                "valid": False,

                "errors": errors

            }

        filename = file.filename

        if is_empty(filename):

            errors["filename"] = "Filename is required."

        elif not validate_file_extension(

            filename,

            {

                "jpg",

                "jpeg",

                "png",

                "pdf"

            }

        ):

            errors["file"] = (

                "Only JPG, JPEG, PNG and PDF files are allowed."

            )

        return {

            "valid": len(errors) == 0,

            "errors": errors

        }


# =====================================================
# Profile Update Validation
# =====================================================

    def validate_profile_update(self, data):

        errors = {}

        name = clean_string(

            data.get("name", "")

        )

        phone = clean_string(

            data.get("phone", "")

        )

        email = clean_string(

            data.get("email", "")

        ).lower()

        if not is_empty(name):

            if not validate_name(name):

                errors["name"] = "Invalid name."

        if not is_empty(email):

            if not validate_email(email):

                errors["email"] = "Invalid email."

        if not is_empty(phone):

            if not validate_phone(phone):

                errors["phone"] = "Invalid phone number."

        return {

            "valid": len(errors) == 0,

            "errors": errors

        }


# =====================================================
# Change Password Validation
# =====================================================

    def validate_change_password(self, data):

        errors = {}

        old_password = data.get(

            "old_password",

            ""

        )

        new_password = data.get(

            "new_password",

            ""

        )

        confirm_password = data.get(

            "confirm_password",

            ""

        )

        if is_empty(old_password):

            errors["old_password"] = (

                "Current password is required."

            )

        if not validate_password(new_password):

            errors["new_password"] = (

                "Password must contain at least "

                "8 characters, uppercase, "

                "lowercase, number and special character."

            )

        if new_password != confirm_password:

            errors["confirm_password"] = (

                "Passwords do not match."

            )

        if old_password == new_password and not is_empty(new_password):

            errors["new_password"] = (

                "New password must be different "

                "from the current password."

            )

        return {

            "valid": len(errors) == 0,

            "errors": errors

        }


# =====================================================
# Admin Action Validation
# =====================================================

    def validate_admin_action(self, data):

        errors = {}

        action = clean_string(

            data.get("action", "")

        )

        allowed_actions = [

            "approve",

            "reject",

            "delete",

            "verify"

        ]

        if action not in allowed_actions:

            errors["action"] = (

                "Invalid admin action."

            )

        return {

            "valid": len(errors) == 0,

            "errors": errors

        }


# =====================================================
# Search Validation
# =====================================================

    def validate_search(self, data):

        errors = {}

        query = clean_string(

            data.get("query", "")

        )

        if is_empty(query):

            errors["query"] = (

                "Search query is required."

            )

        elif len(query) < 2:

            errors["query"] = (

                "Search query must contain at least 2 characters."

            )

        return {

            "valid": len(errors) == 0,

            "errors": errors

        }
    # =====================================================
# Generic Required Fields Validation
# =====================================================

    def validate_required_fields(

        self,

        data,

        required_fields

    ):

        errors = {}

        for field in required_fields:

            if is_empty(

                data.get(field)

            ):

                errors[field] = (

                    f"{field} is required."

                )

        return {

            "valid": len(errors) == 0,

            "errors": errors

        }


    # =================================================
    # Generic Validation Summary
    # =================================================

    def validation_summary(

        self,

        validation_result

    ):

        return {

            "success": validation_result["valid"],

            "total_errors": len(

                validation_result["errors"]

            ),

            "errors": validation_result["errors"]

        }


    # =================================================
    # Health Check
    # =================================================

    def health_check(self):

        return {

            "module": "utils.validators",

            "status": "Running",

            "validator": "Validator"

        }


# =====================================================
# Singleton Instance
# =====================================================

validator = Validator()


# =====================================================
# Wrapper Functions
# =====================================================

def validate_registration(data):

    return validator.validate_registration(data)


def validate_login(data):

    return validator.validate_login(data)


def validate_incident(data):

    return validator.validate_incident(data)


def validate_weather_request(data):

    return validator.validate_weather_request(data)


def validate_prediction(data):

    return validator.validate_prediction(data)


def validate_route(data):

    return validator.validate_route(data)


def validate_file_upload(file):

    return validator.validate_file_upload(file)


def validate_profile_update(data):

    return validator.validate_profile_update(data)


def validate_change_password(data):

    return validator.validate_change_password(data)


def validate_admin_action(data):

    return validator.validate_admin_action(data)


def validate_search(data):

    return validator.validate_search(data)


def validate_required_fields(

    data,

    required_fields

):

    return validator.validate_required_fields(

        data,

        required_fields

    )


def validation_health():

    return validator.health_check()


# =====================================================
# Test Validator
# =====================================================

if __name__ == "__main__":

    print("=" * 50)
    print("PAHADSURAKSHA Validators")
    print("=" * 50)

    print()

    print(

        validation_health()

    )