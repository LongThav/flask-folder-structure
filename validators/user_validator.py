from marshmallow import Schema, fields

class AddUserValidator(Schema):
    fname = fields.Str(required=True, error_messages={"required": "fname is required."})
    lname = fields.Str(required=True, error_messages={"required": "lname is required."})
    email = fields.Str(required=True, error_messages={"required": "email is required."})
    phone = fields.Str(required=True, error_messages={"required": "phone is required."})
    role_id = fields.Int(required=True, error_messages={"required": "role_id is required."})
    password = fields.Str(required=True, error_messages={"required": "password is required."})
    

add_user_validator = AddUserValidator()

class UpdateUserValidator(Schema):
    fname = fields.Str(required=True, error_messages={"required": "fname is required."})
    lname = fields.Str(required=True, error_messages={"required": "lname is required."})
    email = fields.Str(required=True, error_messages={"required": "email is required."})
    phone = fields.Str(required=True, error_messages={"required": "phone is required."})
    role_id = fields.Int(required=True, error_messages={"required": "role_id is required."})
    

update_user_validator = UpdateUserValidator()