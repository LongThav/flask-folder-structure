from urllib import response
import uuid
from flask import jsonify
from marshmallow import ValidationError
# from app import db
import os
import base64
from werkzeug.exceptions import BadRequest

from __init__ import db
from validators import format_validation_errors
from validators.home_validator import assigned_schema, create_schema, role_schema

from models.__init__ import *
from constants.rule_enum import *

from flask import request, jsonify
from sqlalchemy import and_
from validators.user_validator import add_user_validator, update_user_validator



def selectUser():
    try:
        # Get the email search parameter from the request
        email = request.args.get('email')
        
        # Base query
        query = db.session.query(User, Role).join(Role, User.role_id == Role.id).filter(User.dectivate == 1)
        
        # Apply email filter if the parameter is provided
        if email:
            query = query.filter(User.email.ilike(f"%{email}%"))
        
        users = query.all()
        user_data = []
        
        for user, role in users:
            data = {
                'id': user.id,
                'fname': user.fname,
                'lname': user.lname,
                'email': user.email,
                'phone': user.phone,
                'role': {
                    'id': role.id,
                    'title': role.title,
                    'description': role.description,
                    'created_at': role.created_at,
                    'rule': role.rule
                },
                'image': user.image
            }
            user_data.append(data)
        
        return jsonify({
            'msg': 'Response successfully.',
            'status_code': 200,
            'data': user_data
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 400

    
def addUser(data):
    try:
        validatorUser = add_user_validator.load(data)
    except ValidationError as err:
        formatted_errors = format_validation_errors(err.messages)
        return jsonify(formatted_errors), 400
    try:
        obj = User(
            fname = validatorUser['fname'],
            lname = validatorUser['lname'],
            email = validatorUser['email'],
            phone = validatorUser['phone'],
            password = validatorUser['password'],
            role_id = validatorUser['role_id'],
            dectivate = 1
        )
        
        db.session.add(obj)
        db.session.commit()
        
        return jsonify({
            "status_code": 200,
            "message": "User create successfully",
            "data": obj.serialize()
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
def updateUser(user_id, data):
    try:
        # Validate the input data
        validated_data = update_user_validator.load(data)
    except ValidationError as err:
        formatted_errors = format_validation_errors(err.messages)
        return jsonify(formatted_errors), 400

    try:
        # Retrieve the existing user from the database
        user = User.query.get(user_id)
        if user is None:
            return jsonify({"error": "User not found"}), 404

        # Update the user's information
        user.fname = validated_data.get('fname', user.fname)
        user.lname = validated_data.get('lname', user.lname)
        user.email = validated_data.get('email', user.email)
        user.phone = validated_data.get('phone', user.phone)
        # user.password = validated_data.get('password', user.password)
        user.role_id = validated_data.get('role_id', user.role_id)

        # Commit the changes to the database
        db.session.commit()

        return jsonify({
            "status_code": 200,
            "message": "User updated successfully",
            "data": user.serialize()
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 400


def deleteUser(id):
    try:
        # Get the role object by ID
        user = User.query.get(id)
        if not user:
            return jsonify({"error": "User not found"}), 404

        # Update the rule attribute to 0 (inactive)
        user.dectivate = 0

        # Commit the change to the database
        db.session.commit()

        return jsonify({"message": "User deleted successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 400

# def addUser(data):
#     try:
#         validatorUser = add_user_validator.load(data)
#     except ValidationError as err:
#         formatted_errors = format_validation_errors(err.messages)
#         return jsonify(formatted_errors), 400
    
#     try:
#         # Decode base64 image if it's present
#         image_data = data.get('image', '')  # Get image data or empty string if not present
#         if image_data:
#             image_data = image_data.split(",")[-1]  # Remove data URL prefix if present
#             image_binary = base64.b64decode(image_data)
            
#             # Write image to file
#             image_filename = "user_image_{}.png".format(uuid.uuid4().hex)  # Generate a unique filename
#             image_path = os.path.join("uploads/images", image_filename)  # Define the path to save the image
#             with open(image_path, "wb") as f:
#                 f.write(image_binary)
#         else:
#             image_path = None  # No image provided
        
#         # Create User object
#         obj = User(
#             fname = validatorUser['fname'],
#             lname = validatorUser['lname'],
#             email = validatorUser['email'],
#             phone = validatorUser['phone'],
#             password = validatorUser['password'],
#             role_id = validatorUser['role_id'],
#             image = image_path  # Save the image path to the database or None if no image provided
#         )
        
#         db.session.add(obj)
#         db.session.commit()
        
#         return jsonify({
#             "status_code": 200,
#             "message": "User created successfully",
#             "data": obj.serialize()
#         })
    
#     except Exception as e:
#         # Rollback database changes if any error occurs
#         db.session.rollback()
#         return jsonify({"error": str(e)}), 500
