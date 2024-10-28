from validators import auth_validator, home_validator
from validators.user_validator import AddUserValidator


def format_validation_errors(errors):
    formatted_errors = {}
    for field, messages in errors.items():
        formatted_errors[field] = messages[0]  # Use the first error message for each field
    return formatted_errors