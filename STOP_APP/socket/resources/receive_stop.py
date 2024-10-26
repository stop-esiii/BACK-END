from STOP_APP.socket.models import storage_stop


def handle_receive_stop(socketio, data):
    # Get lobby in storage
    storage = storage_stop[f"{data['code_lobby']}"]

    # Append user data
    storage.append({
        "username": data["username"],
        "score": 0,
        "receive_payload": {
            "category_1": data["category_1"],
            "category_2": data["category_2"],
            "category_3": data["category_3"],
            "category_4": data["category_4"],
            "category_5": data["category_5"],
            "category_6": data["category_6"],
            "category_7": data["category_7"],
            "category_8": data["category_8"],
            "category_9": data["category_9"],
            "category_10": data["category_10"]
        }
    })
