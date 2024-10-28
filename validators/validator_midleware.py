from flask import request, jsonify
from marshmallow import ValidationError

from home_validator import AssignedTaskValidator
from controllers.home_controller import assignedTask

assigned_schema = AssignedTaskValidator()

def handle_assigned_task(func):
    def wrapper(*args, **kwargs):
        try:
            # Check if the request data is in JSON format
            if request.content_type == 'application/json':
                # If JSON, directly load the data
                task_data = request.get_json()
            else:
                # If not JSON, assume it's form-encoded and convert it to a dictionary
                task_data = request.form.to_dict(flat=False)

            # Validate the data using the schema
            validated_task = assigned_schema.load(task_data)

            # Call the controller function with validated data
            return assignedTask(validated_task)
        except ValidationError as err:
            # Handle validation errors
            formatted_errors = err.messages
            return jsonify(formatted_errors), 400

    return wrapper
