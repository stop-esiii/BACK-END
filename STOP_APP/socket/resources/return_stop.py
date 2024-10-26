from STOP_APP.sql.services import LobbyService


def handle_return_stop(socketio, data):

    # Search words at the lobby.
    result = LobbyService().return_storage_stop(data["code_lobby"])

    # Emit all words to users validations
    socketio.emit("return_stop",
                  result,
                  to=data["code_lobby"])

    return True
