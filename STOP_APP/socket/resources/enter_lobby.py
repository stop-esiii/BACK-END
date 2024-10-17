from flask_socketio import join_room
from STOP_APP.sql.services import LobbyService


def handle_enter_lobby(socketio, data):
    # Persist lobby
    result = LobbyService().enter_lobby(data)
    if not result["status"]:
        # Return data for Front-End
        socketio.emit("enter_lobby", {
            "status": False,
            "msg": result["msg"]
            },
            to=data["code_lobby"]
        )
        return False

    # Appending client to the room
    join_room(result["lobby"].code_lobby)

    # Return data for Front-End
    socketio.emit("enter_lobby", {
        "msg": "Entrou na sala",
        "time": result["lobby"].time,
        "rounds": result["lobby"].rounds,
        "max_members": result["lobby"].max_members,
        "number_members": result["lobby"].number_members,
        "themes": result["lobby"].themes.split(", ")
        },
        to=result["lobby"].code_lobby
    )
