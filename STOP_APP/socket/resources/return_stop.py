from STOP_APP.sql.services import LobbyService
from STOP_APP.socket.models import storage_stop
import json, logging


def handle_return_stop(socketio, data):

    logging.warning(storage_stop)
    # Get and process the list of players from the specific lobby in one step
    result = sorted(
        [{"username": player["username"], "score": player["score"]} for player in storage_stop[f"{data['code_lobby']}"]],
        key=lambda x: x["score"],
        reverse=True
    )

    # Output the result with "socketio.emit"
    socketio.emit("return_stop", {
        "result": result
        },
        to=data["code_lobby"]
    )
