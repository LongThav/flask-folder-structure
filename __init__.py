from datetime import timedelta
from flask import Flask, Response, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity, verify_jwt_in_request
from flask_cors import CORS
import secrets

from config import *

# Create the Flask application instance
app = Flask(__name__)
CORS(app, supports_credentials=True)  # Allow credentials in CORS headers

# Configure the database URI
app.config['SQLALCHEMY_DATABASE_URI'] = CONNECTION
# Initialize the SQLAlchemy object
db = SQLAlchemy(app)
# Initialize the migration engine
migrate = Migrate(app, db)

# Generate a secure random secret key
jwt_secret_key = secrets.token_urlsafe(32)

app.config['JWT_SECRET_KEY'] = SECRET_KEY
jwt = JWTManager(app)
# Configure JWT expiration times
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=5)  # Access token expires in 1 hour
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=30)  # Refre

app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']


# Middleware to handle routes that require authentication
@app.before_request
def handle_preflight():
    if request.method == "OPTIONS":
        res = Response()
        res.headers['X-Content-Type-Options'] = '*'
        return res
        
def check_jwt_token():
    # Define routes that do not require authentication
    excluded_routes = ['/auth/login', '/auth/register']
    if request.path in excluded_routes:
        return
    # Check for JWT token in the request headers
    try:
        verify_jwt_in_request()
        user_id = get_jwt_identity()
    except Exception as e:
        return jsonify({'message': str(e)}), 401

# Import routes after creating the app instance to avoid circular import
from routes.__init__ import *

# Register the user routes with the Flask app
app.register_blueprint(user_route, url_prefix='/api')
app.register_blueprint(auth_route, url_prefix='/auth')
app.register_blueprint(home_render)
