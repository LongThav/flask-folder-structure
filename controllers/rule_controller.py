from urllib import response
from flask import jsonify
from marshmallow import ValidationError
# from app import db

from __init__ import db
from validators import format_validation_errors
from validators.home_validator import assigned_schema, create_schema, role_schema

from models.__init__ import *
from constants.rule_enum import *

from flask import request, jsonify
from sqlalchemy import and_

def allRole():
    # Get the search query parameter
    search_query = request.args.get('title', None)

    # Construct the query
    query = Role.query.filter_by(rule=1)
    
    # If a search query is provided, add a filter for the title
    if search_query:
        query = query.filter(Role.title.ilike(f'%{search_query}%'))

    # Execute the query
    roles = query.all()
    
    if roles:
        role_list = []
        for role in roles:
            role_data = {
                'id': role.id,
                'title': role.title,
                'description': role.description,
                'rule': role.rule,
                'created_at': role.created_at.strftime('%Y-%m-%d %H:%M:%S') if role.created_at else None
            }
            role_list.append(role_data)
        return jsonify({
            'msg': 'Response successfully.',
            'status_code': 200,
            'data': role_list
        })
    else:
        return jsonify({'error': 'No roles found'}), 404



    
    
    
def createRole(data):
    try:
        validator_role = role_schema.load(data)
    except ValidationError as err:
        formatted_errors = format_validation_errors(err.messages)
        return jsonify(formatted_errors), 400
    try:
        create_role = Role(
            title = validator_role['title'],
            description = validator_role['description'],
            rule=ONE
        )
        
        db.session.add(create_role)
        db.session.commit()
        
        return jsonify({
            "status_code": 200,
            "message": "Role create successfully",
            "data": create_role.serialize()
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
    
def deleteRole(id):
    try:
        # Get the role object by ID
        role = Role.query.get(id)
        if not role:
            return jsonify({"error": "Role not found"}), 404

        # Update the rule attribute to 0 (inactive)
        role.rule = 0

        # Commit the change to the database
        db.session.commit()

        return jsonify({"message": "Role deleted successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 400

def updateRole(id, data):
    try:
        # Validate the input data
        validator_role = role_schema.load(data)
    except ValidationError as err:
        # Return validation errors if any
        formatted_errors = format_validation_errors(err.messages)
        return jsonify(formatted_errors), 400

    try:
        # Get the role object by ID
        role = Role.query.get(id)
        if not role:
            return jsonify({"error": "Role not found"}), 404

        # Update the title and description fields if present in the data
        if 'title' in data:
            role.title = data['title']
        if 'description' in data:
            role.description = data['description']

        # Commit the changes to the database
        db.session.commit()

        return jsonify({
            "status_code": 200,
            "message": "Role updated successfully",
            "data": role.serialize()
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 400