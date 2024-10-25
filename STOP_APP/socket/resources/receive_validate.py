def handle_receive_validate(socketio, data):
    lobby = data["code_lobby"]
    socketio.emit("trigger_stop", to=lobby)
