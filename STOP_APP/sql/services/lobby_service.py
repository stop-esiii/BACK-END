from flask import current_app
from STOP_APP.sql.services import Service
from STOP_APP.sql.repository import LobbyRepository
from STOP_APP.sql.models import Lobby
from STOP_APP.extensions import db
from sqlalchemy import or_
from datetime import datetime


service = Service()


class LobbyService(LobbyRepository):

    model = Lobby()

    def create_lobby(self, data, code_lobby):
        return self.add_lobby(data, code_lobby)
