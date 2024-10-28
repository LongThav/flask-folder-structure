from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from controllers.auth_controller import login, register, logout, profile

auth_route = Blueprint('auth_route', __name__)

@auth_route.route('/login', methods=['POST'])
def login_route():
    return login()

@auth_route.route('/register', methods=['POST'])
def register_user():
    data = request.json
    return register(data)

@auth_route.route('/logout', methods = ['POST'])
@jwt_required()
def logout_user():
    return logout()

@auth_route.route('/profile/<int:id>', methods = ['GET'])
@jwt_required()
def profileUser(id):
    return profile(id)
