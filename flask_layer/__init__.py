from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_layer.client_socket import client_socket
from flask_user import UserManager, SQLAlchemyAdapter
from flask_login import current_user, login_required
from flask_socketio import SocketIO, emit, join_room, leave_room

# from flask_layer.SockUsers import SockUsers

app = Flask(__name__)
app.config.from_object('flask_layer.config')

db = SQLAlchemy(app)
socketio = SocketIO(app)

# Dictionary for saving users socket info
user_sockets = dict()

from flask_layer.models import User

mail = Mail(app)

db.create_all()

db_adapter = SQLAlchemyAdapter(db, User)  # Register the User model
user_manager = UserManager(db_adapter, app)  # Initialize Flask-User


def create_user_sockets_room_dict(name, sid):
    if not user_sockets[name]:
        user_sockets[name] = sid

# TODO Seperate ROOT route from lobby route
@app.route('/')
def lobby_page():
    data = {'item': 'LOBBY', 'action': 'get_lobby', 'data': []}
    context = client_socket(data)
    return render_template('index.html', context=context)

@socketio.on('create table')
@login_required
def create_table(data):
    payload = [current_user.username, data[stack],
            data[table_name], data[seats],
            data[sb_amount], data[bb_amount],
            data[buy_in], data[ante]]
    room = data[table_name]

    create_user_sockets_room_dict(current_user.username, request.sid)

    join_room(room)

    response = client_socket({'item': 'LOBBY', 'action': 'create_table',
                              'data': payload})
    emit(response, room=room)

@socketio.on('view table')
def view_table(data):
    room = data[table_name]
    join_room(room)
    response = client_socket({'item': 'LOBBY', 'action': 'view_table', 'data': room})
    for player in response[players]:
        del player[-2:]
    emit(response, room=room)

@socketio.on('leave table')
def leave_table(data):
    leave_room(data[table_name])

@socketio.on('join table')
@login_required
def join_table(data):
    payload = [data[seat], current_user.username, data[stack]]

    create_user_sockets_room_dict(current_user.username, request.sid)


#
# if __name__ == '__main__':
#     socketio.run(app)
