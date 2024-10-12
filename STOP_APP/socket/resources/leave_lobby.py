from flask_socketio import leave_room
from STOP_APP.sql.services import LobbyService


def handle_leave_lobby(socketio, data):
    # Persist lobby
    result = LobbyService().leave_lobby(data)
    if not result["status"]:
        raise Exception(result["msg"])

    # Remove client of the room
    leave_room(result["lobby"].code_lobby)

    # Return data for Front-End
    socketio.emit("leave_lobby", {
        "msg": f"{result['username']} saiu"
        },
        to=result["lobby"].code_lobby
    )
