# for template
from flask import Blueprint, jsonify, render_template, request

from controllers.home_controller import list_groups_by_all_user

home_render = Blueprint('home_render', __name__)

@home_render.route('/', methods=['GET'])
def group_by_all_user_html():
    # Call the controller function to get data
    data = list_groups_by_all_user(request)

    # Check if the request is for JSON data
    if request.path.endswith('/json'):
        # Return JSON response
        return jsonify(data)
    
    # Return HTML rendering
    return render_template('index.html', users_data=data)