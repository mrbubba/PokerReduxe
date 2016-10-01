from flask import render_template
from flask_layer import db, app, UserManager, db_adapter
from flask_user import login_required
from flask_layer.client_socket import client_socket


@app.route('/')
def lobby_page():
    data = {'item': 'LOBBY', 'action': 'get_lobby', 'data': []}
    context = client_socket(data)

    return render_template('index.html', context)
