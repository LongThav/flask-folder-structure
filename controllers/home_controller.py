from urllib import response
from flask import jsonify
from marshmallow import ValidationError
# from app import db

from __init__ import db
from validators import format_validation_errors
from validators.home_validator import assigned_schema, create_schema
# from models.task_model import Task
# from models.group_model import Group
# from models.user_model import User

from models import Task, Group, User


def get_users():
    users = User.query.all()
    if not users:
        return jsonify({"message": "No users found"}), 404
    return jsonify([user.serialize() for user in users]), 200

def assignedTask(task_data):
    
    try:
        # Load and validate task data
        validated_task = assigned_schema.load(task_data)
    except ValidationError as err:
        formatted_errors = format_validation_errors(err.messages)
        return jsonify(formatted_errors), 400

    try:
        # Create Task object using validated data
        assigned_task = Task(
            title=validated_task['title'],
            description=validated_task['description'],
            priority='Medium',  # You can set default values here
            status='Open',      # You can set default values here
            # due_date=validated_task['due_date'],
            user_id=validated_task['user_id'],
            group_id = validated_task['group_id']
        )

        # Add and commit to the database
        db.session.add(assigned_task)
        db.session.commit()

        # Return success response
        return jsonify({
            "status_code": 200,
            "message": "Task created successfully.",
            "data": assigned_task.serialize()  # Assuming Task has a serialize method
        }), 200
    except Exception as e:
        # Return error response
        return jsonify({"error": str(e)}), 400
    
def allTask():
    task = Task.query.all()
    if not task:
        return jsonify({"message": "No users found"}), 404
    
    serialized_tasks = [tasks.serialize() for tasks in task]
    # Return success response
    return jsonify({
            "status_code": 200,
            "message": "Response successfully.",
            "data": serialized_tasks # Assuming Task has a serialize method
        }), 200

def CreateGroup(data):
    try:
        # Load and validate group data
        validated_data = create_schema.load(data)
        
        # Create group
        group = Group(
            title=validated_data['title'],
            description=validated_data.get('description'),  # Get description if provided
            status='Owner',
            # due_date=validated_data['due_date'],
            user_id=validated_data['user_id']
        )

        # Add and commit to the database
        db.session.add(group)
        db.session.commit()

        return jsonify({
            "status_code": 200,
            "message": "Group created successfully.",
            "data": group.serialize()  # Assuming Group has a serialize method
        }), 200
    except ValidationError as err:
        formatted_errors = format_validation_errors(err.messages)
        return jsonify(formatted_errors), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 400

def list_groups_by_user(user_id):
    # Query the User object by user_id
    user = User.query.get(user_id)

    # Check if the user exists
    if user is None:
        return jsonify({
            "status_code": 404,
            "message": "User not found",
            "data": []
        }), 404

    # Retrieve all groups created by the user
    user_groups = Group.query.filter_by(user_id=user.id).all()

    # Format the groups data
    groups_data = []
    for group in user_groups:
        groups_data.append({
            'id': group.id,
            'title': group.title,
            'description': group.description,
            'status': group.status,
            'due_date': group.due_date.strftime('%Y-%m-%d') if group.due_date else None,
            # Add other fields as needed
        })
    
    # response = jsonify(groups_data)
    # response.headers.add('Access-Control-Allow-Origin', 'http://localhost:5173')
    # response.headers.add('Access-Control-Allow-Methods', 'GET, OPTIONS')
    # response.headers.add('Access-Control-Allow-Headers', 'Authorization')

    return jsonify({
        "status_code": 200,
        "message": "Response successfully.",
        "data": groups_data
    }), 200

# Controller (home_controller.py)
def list_groups_by_all_user(request):
    # Query all User objects
    users = User.query.all()

    # Check if any users exist
    if not users:
        # If the request is for JSON data, return JSON response
        if request.path.endswith('/json'):
            return {
                "status_code": 404,
                "message": "No users found",
                "data": []
            }
        # If the request is for HTML rendering, return an empty list
        return []

    # Collect all users and their groups
    all_users_data = []
    for user in users:
        user_groups = Group.query.filter_by(user_id=user.id).all()

        # Format the groups data for each user
        groups_data = []
        for group in user_groups:
            groups_data.append({
                'id': group.id,
                'title': group.title,
                'description': group.description,
                'status': group.status,
                'due_date': group.due_date.strftime('%Y-%m-%d') if group.due_date else None,
                # Add other fields as needed
            })

        # Add the user and their groups to the collection
        all_users_data.append({
            'user_id': user.id,
            'user_name': user.fname + " " + user.lname,  # Concatenate first name and last name
            'groups': groups_data
        })

    # If the request is for JSON data, return JSON response
    if request.path.endswith('/json'):
        return {
            "status_code": 200,
            "message": "Response successful.",
            "data": all_users_data
        }

    # If the request is for HTML rendering, return the data
    return all_users_data

def list_task_by_group(id):
    group = Group.query.get(id)
    
    if not group:
        return jsonify({
            "status_code": 404,
            "message": "No group found",
            "data": []
        }), 404

    tasks = Task.query.filter_by(group_id=id).order_by(Task.id).all()
    
    task_data = []
    for task in tasks:
        task_data.append({
            "task_id": task.id,
            "task_name": task.title,
            "task_description": task.description,
            "status": task.status,
            "due_date": task.due_date,
            "file": task.file,
            "priority": task.priority
        })
    
    return jsonify({
        "status_code": 200,
        "message": "Tasks retrieved successfully",
        "data": {
            "group_id": group.id,
            "group_name": group.title,
            "group_des": group.description,
            "image": group.image,
            "created_at": group.created_at,
            "tasks": task_data
        }
    }), 200

# https://workingnotworking.com/projects/364826-back-office-cms-dashboard