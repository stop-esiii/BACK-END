from flask import request
from flask_socketio import rooms
from STOP_APP.sql.services import LobbyService


def handle_disconnect_lobby(socketio):
    # Get socket 
    socket_id = request.sid
    # Get rooms of user by sid
    user_rooms = rooms(socket_id)

    # Disconnect client of the rooms
    result = LobbyService().disconnect_lobby(socketio, user_rooms)
    if not result:
        return

    # Return data for Front-End
    socketio.emit("leave_lobby", {
        "msg": f"Alguém saiu"
        },
        to=result
    )
