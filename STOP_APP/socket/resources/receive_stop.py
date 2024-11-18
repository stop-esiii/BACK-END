from STOP_APP.socket.models import storage_stop
from STOP_APP.sql.models import User


def handle_receive_stop(socketio, data):
    # Get lobby in storage
    storage = storage_stop.get(f"{data['code_lobby']}", [])

    # Get username by id_user
    user = User.query.filter(User.id == data["id_user"]).first().username

    # Check if the user is already in storage
    user_entry = next((entry for entry in storage if entry["username"] == user), None)

    if user_entry:
        # Update existing user's data
        user_entry.update({
            "score": user_entry.get("score", 0),  # Retain current score
            "double_points": data["double_points"],
            "autocomplete": data["autocomplete"],
            "receive_payload": data["receive_payload"]
        })
    else:
        # Append new user data
        storage.append({
            "username": user,
            "score": 0,  # Initialize score to 0 for new users
            "double_points": data["double_points"],
            "autocomplete": data["autocomplete"],
            "receive_payload": data["receive_payload"]
        })

    # Save changes
    storage_stop[f"{data['code_lobby']}"] = storage
