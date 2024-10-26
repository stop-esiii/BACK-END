from STOP_APP.socket.models import validations


def handle_receive_validate(socketio, data):
    # Filter lobby by "code_lobby"
    lobby = validations[f"{data['code_lobby']}"]

    # Extract keys
    data.pop("code_lobby", None)

    # Append lobby data
    lobby.append(data)

    # Save data
    validations[f"{data['code_lobby']}"] = lobby
