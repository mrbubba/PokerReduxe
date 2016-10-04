from flask import render_template
from flask_layer import db, app
from flask_user import login_required
from flask_layer.client_socket import client_socket
from flask_user import UserManager, SQLAlchemyAdapter
from flask_layer.models import User


db_adapter = SQLAlchemyAdapter(db, User)  # Register the User model
user_manager = UserManager(db_adapter, app)  # Initialize Flask-User




@app.route('/')
def lobby_page():
    data = {'item': 'LOBBY', 'action': 'get_lobby', 'data': []}
    context = client_socket(data)

    return render_template('index.html', context)
