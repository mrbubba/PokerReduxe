from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_layer.client_socket import client_socket
from flask_user import UserManager, SQLAlchemyAdapter
app = Flask(__name__)
app.config.from_object('flask_layer.config')
db = SQLAlchemy(app)
from flask_layer.models import User


mail = Mail(app)

db.create_all()

db_adapter = SQLAlchemyAdapter(db, User)  # Register the User model
user_manager = UserManager(db_adapter, app)  # Initialize Flask-User

@app.route('/')
def lobby_page():
    data = {'item': 'LOBBY', 'action': 'get_lobby', 'data': []}
    context = client_socket(data)
    return render_template('index.html', context=context)

