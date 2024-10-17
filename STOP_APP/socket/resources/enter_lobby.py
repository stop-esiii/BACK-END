from flask_socketio import join_room
from STOP_APP.sql.services import LobbyService


def handle_enter_lobby(socketio, data):
    # Persist lobby
    result = LobbyService().enter_lobby(data)
    if "status" in result.keys():
        # Return data for Front-End
        socketio.emit("enter_lobby", {
            "status": False,
            "msg": result["msg"]
            },
            to=data["code_lobby"]
        )
        return True

    # Appending client to the room
    join_room(result.code_lobby)

    # Return data for Front-End
    socketio.emit("enter_lobby", {
        "time": result.time,
        "rounds": result.rounds,
        "max_members": result.max_members,
        "number_members": result.number_members + 1,
        "themes": result.themes.split(", ")
        },
        to=result.code_lobby
    )
