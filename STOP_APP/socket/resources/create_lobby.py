from flask_socketio import join_room
from STOP_APP.sql.services import LobbyService
from STOP_APP.socket.models import storage_stop, validations


def handle_create_lobby(socketio, data):
    # Persist lobby
    result = LobbyService().create_lobby(data)

    # Appending client to the room
    join_room(result.code_lobby)

    # Create lobby in storages
    storage_stop.update({f"{result.code_lobby}": []})
    validations.update({f"{result.code_lobby}": []})

    # Return data for Front-End
    socketio.emit("create_lobby", {
        "msg": result.code_lobby,
        "host": data["id_user"],
        "themes": result.themes.split(", ")},
        to=result.code_lobby
    )
