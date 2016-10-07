from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_layer.client_socket import client_socket
from flask_user import UserManager, SQLAlchemyAdapter
from flask_login import current_user, login_required
from flask_socketio import SocketIO, emit, join_room, leave_room
app = Flask(__name__)
app.config.from_object('flask_layer.config')
db = SQLAlchemy(app)
socketio = SocketIO(app)
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


@socketio.on('create table')
@login_required
def create_table(request):
    data = [current_user.username, request[stack],
            request[table_name], request[seats],
            request[sb_amount], request[bb_amount],
            request[buy_in], request[ante]]
    room = request[table_name]
    join_room(room)

    response = client_socket({'item': 'LOBBY', 'action': 'create_table',
                              'data': data})
    emit(response, room=room)

@socketio.on('view table')
def view_table(request):
    room = request[table_name]
    join_room(room)
    response = client_socket({'item': 'LOBBY', 'action': 'view_table', 'data': 'table_name'})
    for player in response[players]:
        del player[-2:]
    emit(response, room=room)

@socketio.on('leave table')
def leave_table(request):
    leave_room(request[table_name])

@socketio.on('join table', )
@login_required
def join_table(request):
    data = [request[seat], current_user.username, request[stack]]




#
#
# @app.route('/')
# def index():
#     return render_template('index.html')
#

# @socketio.on('my event')
# def test_message(message):
#     emit('my response', {'data': 'got it or something'})
#
# if __name__ == '__main__':
#     socketio.run(app)
