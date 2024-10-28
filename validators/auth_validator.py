# schemas.py
from marshmallow import Schema, fields

class LoginValidator(Schema):
    email = fields.Email(required=True, error_messages={"required": "Email is required."})
    password = fields.Str(required=True, error_messages={"required": "Password is required."})

login_schema = LoginValidator()


class RegisterValidator(Schema):
    fname = fields.Str(required=True, error_messages={"required": "First name is required."})
    lname = fields.Str(required=True, error_messages={"required": "Last name is required."})
    email = fields.Email(required=True, error_messages={"required": "Email is required."})
    password = fields.Str(required=True, error_messages={"required": "Password is required."})
    dob = fields.Date(required=True, error_messages={"required": "Date of birth is required."})

register_schema = RegisterValidator()

