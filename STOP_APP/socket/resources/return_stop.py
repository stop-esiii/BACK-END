def handle_return_stop(socketio, data):
    lobby = data["code_lobby"]
    socketio.emit("trigger_stop", to=lobby)
