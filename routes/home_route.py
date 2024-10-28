from flask import Blueprint, render_template,request
from flask_jwt_extended import jwt_required

from controllers.__init__ import *

user_route = Blueprint('user_route', __name__)

@user_route.route('/users', methods=['GET'])
@jwt_required()
def get_users_route():
    return get_users()

@user_route.route('/assigned-task', methods=['POST'])
@jwt_required()
def assigned_task():
    data = request.json
    return assignedTask(data)

@user_route.route('/task', methods=['GET'])
@jwt_required()
def get_all_task():
    return allTask()


@user_route.route('/crate-group', methods=['POST'])
@jwt_required()
def create_group():
    data = request.json
    return CreateGroup(data)

@user_route.route('/group-by-user/<int:id>', methods = ['GET', 'OPTIONS'])
@jwt_required()
def group_by_user(id):
    return list_groups_by_user(id)


@user_route.route('/group-by-user', methods=['GET'])
@jwt_required()
def group_by_all_user():
    return list_groups_by_all_user()

@user_route.route('/task-in-group/<int:id>', methods = ['GET', 'OPTIONS'])
@jwt_required()
def group_task(id):
    return list_task_by_group(id)


@user_route.route('/role', methods=['GET'])
@jwt_required()
def role():
    return allRole()


@user_route.route('/add-role', methods=['POST'])
@jwt_required()
def add_role():
    data = request.json
    return createRole(data)

@user_route.route('/delete-role/<int:id>', methods = ['PUT', 'OPTIONS'])
@jwt_required()
def delete_role(id):
    return deleteRole(id)

@user_route.route('/update-role/<int:id>', methods=['PUT'])
@jwt_required()
def update_role(id):
    data = request.json
    return updateRole(id,data)


@user_route.route('/all-user', methods=['GET'])
@jwt_required()
def all_user():
    return selectUser()


@user_route.route('/add-user', methods=['POST'])
@jwt_required()
def add_user():
    data = request.json
    return addUser(data)

@user_route.route('/update-user/<int:id>', methods=['PUT'])
@jwt_required()
def update_user(id):
    data = request.json
    return updateUser(id,data)

@user_route.route('/delete-user/<int:id>', methods = ['PUT', 'OPTIONS'])
@jwt_required()
def delete_user(id):
    return deleteUser(id)