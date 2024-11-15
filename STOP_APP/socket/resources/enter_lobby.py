from flask_socketio import join_room
from STOP_APP.sql.services import LobbyService
from STOP_APP.sql.models import User
from STOP_APP.socket.models import lobby_users
from sqlalchemy import and_


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

    # Get username by "id_user"
    username = User().query.filter(and_(User.id==data["id_user"], User.active==True)).first().username
    # Get users in lobby_users
    users = lobby_users[f"{data['code_lobby']}"]
    # Append user data
    users.append({
        "id_user": data["id_user"],
        "username": username
    })

    # Save changes
    lobby_users[f"{data['code_lobby']}"] = users

    # Return data for Front-End
    socketio.emit("enter_lobby", {
        "time": int(result["lobby"].time),
        "rounds": result["lobby"].rounds,
        "max_members": result["lobby"].max_members,
        "number_members": result["lobby"].number_members,
        "themes": result["lobby"].themes.split(", "),
        "letters": result["lobby"].letters.split(", "),
        "users": users
        },
        to=result["lobby"].code_lobby
    )
