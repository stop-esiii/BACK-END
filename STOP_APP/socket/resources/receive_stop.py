from STOP_APP.socket.models import storage_stop
from STOP_APP.sql.models import User


def handle_receive_stop(socketio, data):
    # Get lobby in storage
    storage = storage_stop[f"{data['code_lobby']}"]

    # get username by id_user
    user = User().query.filter(
        User.id==data["id_user"]).first().username

    # Append user data
    storage.append({
        "username": user,
        "score": 0,
        "double_points": data["double_points"],
        "autocomplete": data["autocomplete"],
        "receive_payload": data["receive_payload"]
    })

    # Save changes
    storage_stop[f"{data['code_lobby']}"] = storage
