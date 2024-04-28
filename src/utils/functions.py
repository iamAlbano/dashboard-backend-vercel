from datetime import datetime
import re
from werkzeug.security import generate_password_hash, check_password_hash


def is_valid_email(email):
    email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

    return re.match(email_pattern, email)
