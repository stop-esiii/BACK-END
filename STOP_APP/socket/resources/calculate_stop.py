def handle_calculate_stop(socketio, data):
    lobby = data["code_lobby"]
    socketio.emit("trigger_stop", to=lobby)
