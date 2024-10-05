from flask_socketio import join_room
from STOP_APP.app import socketio
from STOP_APP.sql.services import LobbyService
import random
import string


def generate_code(length=4):
    # Defining alphanumeric characters (letters and numbers)
    characters = string.ascii_letters + string.digits
    # Generating a random code with the desired length
    code = ''.join(random.choice(characters) for _ in range(length))
    return code


@socketio.on('join')
def join(data):
    # Create "code_lobby"
    code_lobby = generate_code()
    # Persist lobby
    LobbyService().create_lobby(data, code_lobby)

    join_room(code_lobby)
    return {'msg': f'Código da sala: {code_lobby}.'}
