from marshmallow import Schema, fields

class AssignedTaskValidator(Schema):
    title = fields.Str(required=True, error_messages={"required": "Title is required."})
    description = fields.Str(required=True, error_messages={"required": "Description is required."})
    # due_date = fields.Date(required=True, error_messages={"required": "Due date is required."})
    user_id = fields.Int(required=True, error_messages={"required": "User ID is required."})
    group_id = fields.Int(required=True, error_messages={"required": "Group ID is required."})
    

assigned_schema = AssignedTaskValidator()


class createGroupValidator(Schema):
    title = fields.Str(required=True, error_messages={"required": "Title is required."})
    # due_date = fields.Date(required=True, error_messages={"required": "Due date is required."})
    user_id = fields.Int(required=True, error_messages={"required": "User ID is required."})
    description = fields.Str()
create_schema = createGroupValidator() 


class createRoleValidator(Schema):
    title = fields.Str(required=True, error_messages={"required": "Title is required."})
    description = fields.Str(required=True, error_messages={"required": "Description ID is required."})
role_schema = createRoleValidator() 