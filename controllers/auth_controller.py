# auth_controller.py

from xml.dom import ValidationErr
from flask import jsonify, request
from __init__ import db 
# from flask_jwt_extended import create_access_token, get_jwt
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, jwt_required, get_jwt
from werkzeug.security import generate_password_hash, check_password_hash
# from flask_jwt_extended import jwt_required, get_raw_jwt
from models.user_model import User
from validators import format_validation_errors
from validators.auth_validator import login_schema, register_schema
from marshmallow import ValidationError
from models.revoked_token_model import RevokedToken



def login():
    try:
        # Validate and deserialize input
        data = login_schema.load(request.json)
    except ValidationError as err:
        # Return validation errors in the desired format
        formatted_errors = format_validation_errors(err.messages)
        return jsonify(formatted_errors), 400

    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()

    if user and check_password_hash(user.password, password):
        access_token = create_access_token(identity=user.id)
        return jsonify({
            "status_code": 200,
            "message": "Response successfully.",
            "data": {
                "access_token": access_token,
                "user": user.serialize()
            }
        }), 200
    else:
        return jsonify({"message": "Invalid email or password"}), 401

def register(data):
    try:
        data = register_schema.load(data)  # Validate and deserialize input
    except ValidationError as err:
        formatted_errors = format_validation_errors(err.messages)
        return jsonify(formatted_errors), 400

    try:
        new_user = User(
            fname=data['fname'],
            lname=data['lname'],
            email=data['email'],
            password=generate_password_hash(data['password']),  # Hash password before storing
            dob=data['dob']
        )
        db.session.add(new_user)
        db.session.commit()
        return jsonify({
            "status_code": 200,
            "message": "Response successfully.",
            "data": new_user.serialize()
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

def logout():
    try:
        current_token = get_jwt()
        jti = current_token['jti']
        revoked_token = RevokedToken(jti=jti)
        db.session.add(revoked_token)
        db.session.commit()
        return {'msg': 'Successfully logged out'}, 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500 

def profile(id):
    user = User.query.get(id)
    if user:
        return jsonify({
            'msg': 'Response successfully.',
            'status_code': 200,
            'data' : {
               'id': user.id,
               'email': user.email,
               'fname': user.fname,
               'lname': user.lname,
               'image': user.image,
               'dob': user.dob
            }
            
        })
    else:
        return jsonify({'error': 'User not found'}), 404

    