from STOP_APP.sql.services import LobbyService
from STOP_APP.socket.models import storage_stop


def handle_return_stop(socketio, data):

    # Get the list of players from the specific lobby
    print(storage_stop)
    result = storage_stop[f"{data['code_lobby']}"]

    # Sort by score
    result = sorted(result, key=lambda x: x["score"], reverse=True)

    # Extract only the "username" and "score" of each player
    result = [{"username": player["username"], "score": player["score"]} for player in result]

    # Output the result with "socketio.emit"
    print("=-=RETURN=-=")
    socketio.emit("return_stop", {
        "result": result
        },
        to=data["code_lobby"]
    )
