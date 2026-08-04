import re
import uuid
from datetime import datetime
from flask import jsonify


# =====================================================
# Success Response
# =====================================================

def success_response(

    message="Success",

    data=None,

    status_code=200

):

    response = {

        "success": True,

        "message": message,

        "timestamp": current_timestamp()

    }

    if data is not None:

        response["data"] = data

    return jsonify(

        response

    ), status_code


# =====================================================
# Error Response
# =====================================================

def error_response(

    message="Something went wrong.",

    status_code=400,

    errors=None

):

    response = {

        "success": False,

        "message": message,

        "timestamp": current_timestamp()

    }

    if errors is not None:

        response["errors"] = errors

    return jsonify(

        response

    ), status_code


# =====================================================
# Current Timestamp
# =====================================================

def current_timestamp():

    return datetime.utcnow().isoformat() + "Z"


# =====================================================
# Generate UUID
# =====================================================

def generate_uuid():

    return str(

        uuid.uuid4()

    )


# =====================================================
# Generate Incident ID
# =====================================================

def generate_incident_id():

    timestamp = datetime.utcnow().strftime(

        "%Y%m%d%H%M%S"

    )

    unique = str(

        uuid.uuid4()

    )[:8].upper()

    return f"INC-{timestamp}-{unique}"


# =====================================================
# Format Date
# =====================================================

def format_date(

    date_obj,

    fmt="%d-%m-%Y %H:%M:%S"

):

    if date_obj is None:

        return None

    return date_obj.strftime(

        fmt

    )


# =====================================================
# Convert String to Datetime
# =====================================================

def parse_datetime(

    date_string,

    fmt="%Y-%m-%d %H:%M:%S"

):

    try:

        return datetime.strptime(

            date_string,

            fmt

        )

    except Exception:

        return None


# =====================================================
# Check Empty Value
# =====================================================

def is_empty(value):

    if value is None:

        return True

    if isinstance(value, str):

        return value.strip() == ""

    return False


# =====================================================
# Remove Extra Spaces
# =====================================================

def clean_string(text):

    if text is None:

        return ""

    return " ".join(

        text.strip().split()

    )
# =====================================================
# Email Validation
# =====================================================

def validate_email(email):

    if is_empty(email):

        return False

    pattern = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'

    return re.match(

        pattern,

        email

    ) is not None


# =====================================================
# Password Validation
#
# Minimum:
# 8 Characters
# 1 Uppercase
# 1 Lowercase
# 1 Number
# 1 Special Character
# =====================================================

def validate_password(password):

    if is_empty(password):

        return False

    if len(password) < 8:

        return False

    if not re.search(

        r"[A-Z]",

        password

    ):

        return False

    if not re.search(

        r"[a-z]",

        password

    ):

        return False

    if not re.search(

        r"[0-9]",

        password

    ):

        return False

    if not re.search(

        r"[!@#$%^&*(),.?\":{}|<>]",

        password

    ):

        return False

    return True


# =====================================================
# Phone Number Validation
#
# Indian Mobile Number
# =====================================================

def validate_phone(phone):

    if is_empty(phone):

        return False

    pattern = r"^[6-9]\d{9}$"

    return re.match(

        pattern,

        phone

    ) is not None


# =====================================================
# Latitude Validation
# =====================================================

def validate_latitude(latitude):

    try:

        latitude = float(latitude)

        return -90 <= latitude <= 90

    except Exception:

        return False


# =====================================================
# Longitude Validation
# =====================================================

def validate_longitude(longitude):

    try:

        longitude = float(longitude)

        return -180 <= longitude <= 180

    except Exception:

        return False


# =====================================================
# Coordinate Validation
# =====================================================

def validate_coordinates(

    latitude,

    longitude

):

    return (

        validate_latitude(

            latitude

        )

        and

        validate_longitude(

            longitude

        )

    )


# =====================================================
# Validate Pincode
#
# Indian Postal Code
# =====================================================

def validate_pincode(pincode):

    if is_empty(pincode):

        return False

    pattern = r"^[1-9][0-9]{5}$"

    return re.match(

        pattern,

        str(pincode)

    ) is not None


# =====================================================
# Validate Name
# =====================================================

def validate_name(name):

    if is_empty(name):

        return False

    pattern = r"^[A-Za-z ]{2,100}$"

    return re.match(

        pattern,

        clean_string(name)

    ) is not None


# =====================================================
# Validate City
# =====================================================

def validate_city(city):

    if is_empty(city):

        return False

    return len(

        clean_string(city)

    ) >= 2
import math
import os


# =====================================================
# Calculate Distance (Haversine Formula)
# =====================================================

def calculate_distance(

    lat1,

    lon1,

    lat2,

    lon2

):

    radius = 6371.0

    lat1 = math.radians(float(lat1))
    lon1 = math.radians(float(lon1))
    lat2 = math.radians(float(lat2))
    lon2 = math.radians(float(lon2))

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = (

        math.sin(dlat / 2) ** 2 +

        math.cos(lat1) *

        math.cos(lat2) *

        math.sin(dlon / 2) ** 2

    )

    c = 2 * math.atan2(

        math.sqrt(a),

        math.sqrt(1 - a)

    )

    return round(

        radius * c,

        2

    )


# =====================================================
# Validate File Extension
# =====================================================

def validate_file_extension(

    filename,

    allowed_extensions=None

):

    if allowed_extensions is None:

        allowed_extensions = {

            "jpg",

            "jpeg",

            "png",

            "gif",

            "webp",

            "pdf"

        }

    if "." not in filename:

        return False

    extension = filename.rsplit(

        ".",

        1

    )[1].lower()

    return extension in allowed_extensions


# =====================================================
# Get File Extension
# =====================================================

def get_file_extension(filename):

    if "." not in filename:

        return ""

    return filename.rsplit(

        ".",

        1

    )[1].lower()


# =====================================================
# Convert Bytes
# =====================================================

def format_file_size(size):

    units = [

        "B",

        "KB",

        "MB",

        "GB"

    ]

    index = 0

    while size >= 1024 and index < len(units) - 1:

        size /= 1024

        index += 1

    return f"{size:.2f} {units[index]}"


# =====================================================
# Validate Weather Values
# =====================================================

def validate_weather_data(weather):

    required = [

        "rainfall",

        "humidity",

        "temperature",

        "wind_speed",

        "pressure",

        "visibility"

    ]

    for item in required:

        if item not in weather:

            return False

    return True


# =====================================================
# Safe Float Conversion
# =====================================================

def to_float(value, default=0.0):

    try:

        return float(value)

    except Exception:

        return default


# =====================================================
# Safe Integer Conversion
# =====================================================

def to_int(value, default=0):

    try:

        return int(value)

    except Exception:

        return default


# =====================================================
# Capitalize Text
# =====================================================

def capitalize_words(text):

    if is_empty(text):

        return ""

    return clean_string(

        text

    ).title()


# =====================================================
# Normalize City Name
# =====================================================

def normalize_city(city):

    return capitalize_words(

        city

    )


# =====================================================
# Check File Exists
# =====================================================

def file_exists(filepath):

    return os.path.exists(

        filepath

    )
import json
import logging
import secrets
import string


# =====================================================
# Logger Configuration
# =====================================================

logging.basicConfig(

    level=logging.INFO,

    format="%(asctime)s - %(levelname)s - %(message)s"

)

logger = logging.getLogger(__name__)


# =====================================================
# Log Information
# =====================================================

def log_info(message):

    logger.info(message)


# =====================================================
# Log Warning
# =====================================================

def log_warning(message):

    logger.warning(message)


# =====================================================
# Log Error
# =====================================================

def log_error(message):

    logger.error(message)


# =====================================================
# Convert Dictionary To JSON
# =====================================================

def dict_to_json(data):

    try:

        return json.dumps(

            data,

            indent=4,

            default=str

        )

    except Exception:

        return "{}"


# =====================================================
# Convert JSON To Dictionary
# =====================================================

def json_to_dict(data):

    try:

        return json.loads(data)

    except Exception:

        return {}


# =====================================================
# Generate Secure Random Token
# =====================================================

def generate_token(length=32):

    characters = (

        string.ascii_letters +

        string.digits

    )

    return "".join(

        secrets.choice(characters)

        for _ in range(length)

    )


# =====================================================
# Health Check
# =====================================================

def health_check():

    return {

        "status": "Running",

        "module": "utils.helpers",

        "timestamp": current_timestamp()

    }


# =====================================================
# Environment Information
# =====================================================

def environment_information():

    return {

        "python_version": os.sys.version,

        "platform": os.name,

        "current_directory": os.getcwd()

    }


# =====================================================
# Pagination Helper
# =====================================================

def paginate(items, page=1, per_page=10):

    page = max(1, page)

    per_page = max(1, per_page)

    start = (page - 1) * per_page

    end = start + per_page

    return {

        "page": page,

        "per_page": per_page,

        "total": len(items),

        "data": items[start:end]

    }


# =====================================================
# Safe Dictionary Getter
# =====================================================

def safe_get(dictionary, key, default=None):

    if not isinstance(dictionary, dict):

        return default

    return dictionary.get(

        key,

        default

    )


# =====================================================
# Check Required Fields
# =====================================================

def check_required_fields(data, required_fields):

    missing = []

    for field in required_fields:

        if is_empty(

            data.get(field)

        ):

            missing.append(field)

    return missing


# =====================================================
# Application Version
# =====================================================

def app_version():

    return {

        "application": "PAHADSURAKSHA",

        "version": "1.0.0"

    }