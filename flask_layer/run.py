from flask_layer import app, socketio


app.run(host='127.0.0.1', port=5000, debug=True)
socketio.run(app)