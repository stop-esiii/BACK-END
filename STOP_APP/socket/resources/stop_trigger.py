def handle_stop_trigger(socketio, data):
    lobby = data["code_lobby"]
    socketio.emit("stop_trigger", to=lobby)
