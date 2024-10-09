from flask import current_app
from STOP_APP.sql.services import Service
from STOP_APP.sql.repository import LobbyRepository
from STOP_APP.sql.models import Lobby
from STOP_APP.extensions import db
from sqlalchemy import or_
from datetime import datetime
import random
import string


service = Service()


class LobbyService(LobbyRepository):

    model = Lobby()

    def generate_code(self, length=4):
        # Defining alphanumeric characters (letters and numbers)
        characters = string.ascii_letters + string.digits
        # Generating a random code with the desired length
        code = ''.join(random.choice(characters) for _ in range(length))
        return code

    def create_lobby(self, data, code_lobby):
        # Create "code_lobby"
        code_lobby = self.generate_code()
        # Save Lobby
        return self.add_lobby(data, code_lobby)
