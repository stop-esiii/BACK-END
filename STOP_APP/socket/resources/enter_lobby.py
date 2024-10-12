from flask_socketio import join_room
from STOP_APP.sql.services import LobbyService


def handle_enter_lobby(socketio, data):
    # Persist lobby
    result = LobbyService().enter_lobby(data)
    if not result["status"]:
        raise Exception(result["msg"])

    # Appending client to the room
    join_room(result.code_lobby)

    # Return data for Front-End
    socketio.emit("enter_lobby", {
        "time": result.time,
        "rounds": result.rounds,
        "max_members": result.max_members,
        "number_members": result.number_members,
        "themes": result.themes.split(", ")
        },
        to=result.code_lobby
    )
