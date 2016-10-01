from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_user import UserManager, SQLAlchemyAdapter
from flask_layer.models import User

app = Flask(__name__)
app.config.from_object('config.ConfigClass')

db = SQLAlchemy(app)
mail = Mail(app)

db.create_all()

db_adapter = SQLAlchemyAdapter(db, User)  # Register the User model
user_manager = UserManager(db_adapter, app)  # Initialize Flask-User
