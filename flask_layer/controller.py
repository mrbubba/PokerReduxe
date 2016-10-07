from flask import render_template, request
from flask_layer import db, app
from flask_user import login_required
from flask_login import current_user
from flask_layer.client_socket import client_socket
from flask_user import UserManager, SQLAlchemyAdapter
from flask_layer.models import User


db_adapter = SQLAlchemyAdapter(db, User)  # Register the User model
user_manager = UserManager(db_adapter, app)  # Initialize Flask-User



